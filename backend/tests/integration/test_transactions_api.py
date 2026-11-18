
from app.models.category import Category


def register_and_login(client, email="transaction@example.com"):
    """Register a test user and return their JWT token."""

    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Transaction Test User",
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
    """Create a category for testing."""

    category = Category(
        user_id=user_id,
        name=f"Test {category_type.title()} Category",
        category_type=category_type,
        is_default=True if user_id is None else False,
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


def transaction_payload(category_id, transaction_type="expense", amount="500.00"):
    return {
        "category_id": category_id,
        "amount": amount,
        "transaction_type": transaction_type,
        "description": "Test transaction",
        "transaction_date": "2026-11-18T10:00:00Z",
    }


def test_create_transaction_success(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)

    response = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["amount"] == "500.00"
    assert data["transaction_type"] == "expense"
    assert data["category_id"] == category.id
    assert data["description"] == "Test transaction"


def test_create_income_transaction_success(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session, "income")

    response = client.post(
        "/api/transactions",
        json=transaction_payload(
            category.id,
            transaction_type="income",
            amount="25000.00",
        ),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["transaction_type"] == "income"


def test_create_transaction_rejects_invalid_category(client):
    token = register_and_login(client)

    response = client.post(
        "/api/transactions",
        json=transaction_payload(999),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_create_transaction_rejects_category_type_mismatch(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session, "income")

    response = client.post(
        "/api/transactions",
        json=transaction_payload(
            category.id,
            transaction_type="expense",
        ),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_list_transactions(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    response = client.get("/api/transactions", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_transactions_by_type(client, db_session):
    token = register_and_login(client)
    expense_category = create_category(db_session, "expense")
    income_category = create_category(db_session, "income")
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/transactions",
        json=transaction_payload(expense_category.id, "expense"),
        headers=headers,
    )

    client.post(
        "/api/transactions",
        json=transaction_payload(income_category.id, "income"),
        headers=headers,
    )

    response = client.get(
        "/api/transactions?transaction_type=income",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["transaction_type"] == "income"


def test_retrieve_transaction(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    transaction_id = creation.json()["id"]

    response = client.get(
        f"/api/transactions/{transaction_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id


def test_update_transaction(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    transaction_id = creation.json()["id"]

    response = client.put(
        f"/api/transactions/{transaction_id}",
        json={"amount": "750.00", "description": "Updated transaction"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["amount"] == "750.00"
    assert response.json()["description"] == "Updated transaction"


def test_delete_transaction(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    transaction_id = creation.json()["id"]

    deletion = client.delete(
        f"/api/transactions/{transaction_id}",
        headers=headers,
    )

    assert deletion.status_code == 204

    retrieval = client.get(
        f"/api/transactions/{transaction_id}",
        headers=headers,
    )

    assert retrieval.status_code == 404


def test_user_cannot_access_another_users_transaction(client, db_session):
    first_token = register_and_login(client, "first-user@example.com")
    category = create_category(db_session)

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers={"Authorization": f"Bearer {first_token}"},
    )

    transaction_id = creation.json()["id"]

    second_token = register_and_login(client, "second-user@example.com")

    response = client.get(
        f"/api/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {second_token}"},
    )

    assert response.status_code == 404


def test_transaction_endpoint_requires_authentication(client):
    response = client.get("/api/transactions")

    assert response.status_code == 401


def test_list_transactions_rejects_invalid_date_range(client):
    token = register_and_login(client)

    response = client.get(
        "/api/transactions",
        params={
            "start_date": "2026-11-20T10:00:00Z",
            "end_date": "2026-11-18T10:00:00Z",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


def test_update_transaction_with_empty_payload_is_rejected(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    assert creation.status_code == 201
    transaction_id = creation.json()["id"]

    response = client.put(
        f"/api/transactions/{transaction_id}",
        json={},
        headers=headers,
    )

    assert response.status_code == 422


def test_update_transaction_with_null_amount_is_rejected(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    assert creation.status_code == 201
    transaction_id = creation.json()["id"]

    response = client.put(
        f"/api/transactions/{transaction_id}",
        json={"amount": None},
        headers=headers,
    )

    assert response.status_code == 422


def test_update_transaction_with_null_category_is_rejected(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    creation = client.post(
        "/api/transactions",
        json=transaction_payload(category.id),
        headers=headers,
    )

    assert creation.status_code == 201
    transaction_id = creation.json()["id"]

    response = client.put(
        f"/api/transactions/{transaction_id}",
        json={"category_id": None},
        headers=headers,
    )

    assert response.status_code == 422


def test_update_transaction_can_clear_description(client, db_session):
    token = register_and_login(client)
    category = create_category(db_session)
    headers = {"Authorization": f"Bearer {token}"}

    payload = transaction_payload(category.id)
    payload["description"] = "Test description"

    creation = client.post(
        "/api/transactions",
        json=payload,
        headers=headers,
    )

    assert creation.status_code == 201
    transaction_id = creation.json()["id"]

    response = client.put(
        f"/api/transactions/{transaction_id}",
        json={"description": None},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["description"] is None
