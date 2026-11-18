
from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.category import Category


def register_and_login(client, email="dashboard@example.com"):
    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Dashboard Test User",
            "email": email,
            "password": "TestPassword123!",
            "starting_balance": 10000.00,
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert login.status_code == 200
    return login.json()["access_token"]


def create_category(db_session, name, category_type):
    category = Category(
        user_id=None,
        name=name,
        category_type=category_type,
        is_default=True,
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


def create_transaction(
    client,
    token,
    category_id,
    transaction_type,
    amount,
):
    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    response = client.post(
        "/api/transactions",
        json={
            "category_id": category_id,
            "amount": amount,
            "transaction_type": transaction_type,
            "description": "Dashboard integration test",
            "transaction_date": now.isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    return response


def test_dashboard_empty_account(client):
    token = register_and_login(client)

    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert float(data["starting_balance"]) == 10000.00
    assert float(data["current_balance"]) == 10000.00
    assert float(data["total_income"]) == 0
    assert float(data["total_expenses"]) == 0
    assert float(data["monthly_savings"]) == 0
    assert data["category_spending"] == []


def test_dashboard_calculates_income_expenses_and_balance(
    client,
    db_session,
):
    token = register_and_login(client)

    income_category = create_category(
        db_session, "Test Salary", "income"
    )
    expense_category = create_category(
        db_session, "Test Food", "expense"
    )

    create_transaction(
        client, token, income_category.id, "income", "25000.00"
    )
    create_transaction(
        client, token, expense_category.id, "expense", "5000.00"
    )

    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert float(data["starting_balance"]) == 10000.00
    assert float(data["total_income"]) == 25000.00
    assert float(data["total_expenses"]) == 5000.00
    assert float(data["current_balance"]) == 30000.00
    assert float(data["monthly_income"]) == 25000.00
    assert float(data["monthly_expenses"]) == 5000.00
    assert float(data["monthly_savings"]) == 20000.00


def test_dashboard_category_spending(client, db_session):
    token = register_and_login(client)

    food = create_category(db_session, "Test Food", "expense")
    rent = create_category(db_session, "Test Rent", "expense")

    create_transaction(client, token, food.id, "expense", "1200.00")
    create_transaction(client, token, rent.id, "expense", "8000.00")

    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    spending = response.json()["category_spending"]

    assert len(spending) == 2
    assert spending[0]["category_name"] == "Test Rent"
    assert float(spending[0]["total_amount"]) == 8000.00
    assert spending[1]["category_name"] == "Test Food"
    assert float(spending[1]["total_amount"]) == 1200.00


def test_dashboard_requires_authentication(client):
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 401


def test_dashboard_only_shows_authenticated_users_data(
    client,
    db_session,
):
    first_token = register_and_login(
        client, "first_dashboard@example.com"
    )

    category = create_category(
        db_session, "Test Expense", "expense"
    )

    create_transaction(
        client, first_token, category.id, "expense", "4000.00"
    )

    second_token = register_and_login(
        client, "second_dashboard@example.com"
    )

    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {second_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert float(data["total_expenses"]) == 0
    assert float(data["current_balance"]) == 10000.00
    assert data["category_spending"] == []
