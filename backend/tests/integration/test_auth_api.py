
def test_register_endpoint_success(client):
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Integration Test User",
            "email": "integration@example.com",
            "password": "TestPassword123!",
            "phone_number": "9876543210",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["full_name"] == "Integration Test User"
    assert data["email"] == "integration@example.com"
    assert data["phone_number"] == "9876543210"
    assert "hashed_password" not in data


def test_register_endpoint_without_phone_number(client):
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "No Phone User",
            "email": "no-phone@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201
    assert response.json()["phone_number"] is None


def test_register_endpoint_rejects_duplicate_phone_number(client):
    first_response = client.post(
        "/api/auth/register",
        json={
            "full_name": "First Phone User",
            "email": "first-phone@example.com",
            "password": "TestPassword123!",
            "phone_number": "9876543210",
        },
    )

    second_response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Second Phone User",
            "email": "second-phone@example.com",
            "password": "TestPassword123!",
            "phone_number": "9876543210",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Phone number is already registered"
    )


def test_register_endpoint_rejects_duplicate_email(client):
    user_data = {
        "full_name": "Duplicate Test User",
        "email": "duplicate@example.com",
        "password": "TestPassword123!",
    }

    first_response = client.post(
        "/api/auth/register",
        json=user_data,
    )

    second_response = client.post(
        "/api/auth/register",
        json=user_data,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email is already registered"


def test_login_endpoint_success(client):
    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Login Test User",
            "email": "login-test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert registration.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={
            "email": "login-test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_endpoint_rejects_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={
            "full_name": "Wrong Password User",
            "email": "wrong-password@example.com",
            "password": "CorrectPassword123!",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "wrong-password@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_get_me_endpoint_with_valid_token(client):
    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Authenticated Test User",
            "email": "authenticated-test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert registration.status_code == 201

    login = client.post(
        "/api/auth/login",
        json={
            "email": "authenticated-test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["full_name"] == "Authenticated Test User"
    assert data["email"] == "authenticated-test@example.com"
    assert data["is_active"] is True
    assert "hashed_password" not in data


def test_get_me_endpoint_without_token(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_get_me_endpoint_with_invalid_token(client):
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401
