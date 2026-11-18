
from app.models.category import Category


def register_and_login(client, email="budget@example.com"):
    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Budget Test User",
            "email": email,
            "password": "TestPassword123!",
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


def create_category(db_session, category_type="expense", user_id=None):
    category = Category(
        user_id=user_id,
        name=f"Test {category_type.title()} Category",
        category_type=category_type,
        is_default=user_id is None,
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


def budget_payload(category_id, amount="5000.00"):
    return {
        "category_id": category_id,
        "amount": amount,
        "month": 11,
        "year": 2026,
    }


def test_create_budget_success(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/budgets",
        json=budget_payload(category.id),
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["category_id"] == category.id
    assert data["amount"] == "5000.00"
    assert data["month"] == 11
    assert data["year"] == 2026


def test_create_budget_rejects_duplicate(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}
    payload = budget_payload(category.id)

    first = client.post("/api/budgets", json=payload, headers=headers)
    second = client.post("/api/budgets", json=payload, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 400


def test_create_budget_rejects_income_category(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session, "income")

    response = client.post(
        "/api/budgets",
        json=budget_payload(category.id),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_create_budget_rejects_invalid_category(client):
    token = register_and_login(client)

    response = client.post(
        "/api/budgets",
        json=budget_payload(999),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_list_budgets(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/budgets",
        json=budget_payload(category.id),
        headers=headers,
    )

    response = client.get(
        "/api/budgets",
        params={"month": 11, "year": 2026},
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category_id"] == category.id


def test_budget_progress_calculates_spending(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    budget = client.post(
        "/api/budgets",
        json=budget_payload(category.id, "5000.00"),
        headers=headers,
    )
    assert budget.status_code == 201

    transaction = client.post(
        "/api/transactions",
        json={
            "category_id": category.id,
            "amount": "1200.00",
            "transaction_type": "expense",
            "description": "Test spending",
            "transaction_date": "2026-11-18T10:00:00Z",
        },
        headers=headers,
    )
    assert transaction.status_code == 201

    response = client.get(
        f"/api/budgets/{budget.json()['id']}",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["spent"] == "1200.00"
    assert data["remaining"] == "3800.00"
    assert data["percentage_used"] == 24.0
    assert data["is_exceeded"] is False


def test_update_budget(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/budgets",
        json=budget_payload(category.id),
        headers=headers,
    )
    budget_id = creation.json()["id"]

    response = client.put(
        f"/api/budgets/{budget_id}",
        json={"amount": "7000.00"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["amount"] == "7000.00"


def test_delete_budget(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/budgets",
        json=budget_payload(category.id),
        headers=headers,
    )
    budget_id = creation.json()["id"]

    deletion = client.delete(
        f"/api/budgets/{budget_id}",
        headers=headers,
    )
    assert deletion.status_code == 204

    retrieval = client.get(
        f"/api/budgets/{budget_id}",
        headers=headers,
    )
    assert retrieval.status_code == 404


def test_user_cannot_access_another_users_budget(client, db_session):
    first_token = register_and_login(client, "first-budget@example.com")
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {first_token}"}

    creation = client.post(
        "/api/budgets",
        json=budget_payload(category.id),
        headers=headers,
    )
    budget_id = creation.json()["id"]

    second_token = register_and_login(client, "second-budget@example.com")

    response = client.get(
        f"/api/budgets/{budget_id}",
        headers={"Authorization": f"Bearer {second_token}"},
    )

    assert response.status_code == 404


def test_budget_endpoint_requires_authentication(client):
    response = client.get("/api/budgets")
    assert response.status_code == 401
