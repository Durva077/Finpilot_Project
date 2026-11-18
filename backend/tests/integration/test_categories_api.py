
from sqlalchemy import select

from app.models.category import Category
from app.models.user import User
from app.services.category_service import seed_default_categories


def register_and_login(client, email):
    """Register a test user and return their JWT token."""
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Category Test User",
            "email": email,
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "TestPassword123!",
        },
    )
    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def create_custom_category(db_session, email, name, category_type):
    """Create a category owned by a specific test user."""
    user = db_session.scalar(
        select(User).where(User.email == email)
    )
    assert user is not None

    category = Category(
        user_id=user.id,
        name=name,
        category_type=category_type,
        is_default=False,
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


def test_list_categories_returns_default_categories(client, db_session):
    seed_default_categories(db_session)
    token = register_and_login(client, "defaults@example.com")

    response = client.get(
        "/api/categories",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    categories = response.json()
    assert len(categories) > 0
    assert any(category["is_default"] for category in categories)


def test_category_type_filter_returns_only_matching_categories(
    client, db_session
):
    seed_default_categories(db_session)
    token = register_and_login(client, "filter@example.com")

    response = client.get(
        "/api/categories",
        params={"category_type": "income"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    categories = response.json()
    assert len(categories) > 0
    assert all(
        category["category_type"] == "income"
        for category in categories
    )


def test_user_sees_own_custom_categories_not_other_users(
    client, db_session
):
    seed_default_categories(db_session)

    token_one = register_and_login(client, "first@example.com")
    register_and_login(client, "second@example.com")

    create_custom_category(
        db_session, "first@example.com", "My Custom Food", "expense"
    )
    create_custom_category(
        db_session, "second@example.com", "Private Category", "expense"
    )

    response = client.get(
        "/api/categories",
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 200
    names = [category["name"] for category in response.json()]

    assert "My Custom Food" in names
    assert "Private Category" not in names


def test_list_categories_requires_authentication(client, db_session):
    seed_default_categories(db_session)

    response = client.get("/api/categories")

    assert response.status_code == 401


def test_invalid_category_type_returns_422(client):
    token = register_and_login(client, "invalid@example.com")

    response = client.get(
        "/api/categories",
        params={"category_type": "invalid"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_default_category_seeding_is_idempotent(db_session):
    seed_default_categories(db_session)

    first_count = db_session.query(Category).filter(
        Category.user_id.is_(None),
        Category.is_default.is_(True),
    ).count()

    seed_default_categories(db_session)

    second_count = db_session.query(Category).filter(
        Category.user_id.is_(None),
        Category.is_default.is_(True),
    ).count()

    assert first_count > 0
    assert first_count == second_count


def test_expense_filter_returns_only_expense_categories(
    client, db_session
):
    seed_default_categories(db_session)
    token = register_and_login(client, "expense@example.com")

    response = client.get(
        "/api/categories",
        params={"category_type": "expense"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    categories = response.json()
    assert len(categories) > 0
    assert all(
        category["category_type"] == "expense"
        for category in categories
    )
