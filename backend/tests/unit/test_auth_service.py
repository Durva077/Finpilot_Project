from unittest.mock import MagicMock, patch
from app.services.auth_service import login_user
import pytest

from app.models.user import User
from app.schemas.auth import UserRegister
from app.services.auth_service import register_user


def test_register_user_success():
    db = MagicMock()
    db.scalar.return_value = None

    user_data = UserRegister(
        full_name="Test User",
        email="test@example.com",
        password="TestPassword123!",
    )

    with patch(
        "app.services.auth_service.hash_password",
        return_value="hashed_test_password",
    ):
        result = register_user(db, user_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)

    assert isinstance(result, User)
    assert result.full_name == "Test User"
    assert result.email == "test@example.com"
    assert result.hashed_password == "hashed_test_password"


def test_register_user_rejects_duplicate_email():
    db = MagicMock()
    db.scalar.return_value = User(
        full_name="Existing User",
        email="test@example.com",
        hashed_password="existing_hash",
    )

    user_data = UserRegister(
        full_name="New User",
        email="test@example.com",
        password="TestPassword123!",
    )

    with pytest.raises(ValueError, match="Email is already registered"):
        register_user(db, user_data)

    db.add.assert_not_called()
    db.commit.assert_not_called()

def test_login_user_success():
    db = MagicMock()

    user = User(
        id=1,
        full_name="Test User",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    db.scalar.return_value = user

    with patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ), patch(
        "app.services.auth_service.create_access_token",
        return_value="test.jwt.token",
    ):
        result = login_user(db, "test@example.com", "TestPassword123!")

    assert result.access_token == "test.jwt.token"
    assert result.token_type == "bearer"


def test_login_user_rejects_invalid_password():
    db = MagicMock()

    user = User(
        id=1,
        full_name="Test User",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    db.scalar.return_value = user

    with patch(
        "app.services.auth_service.verify_password",
        return_value=False,
    ):
        with pytest.raises(ValueError, match="Invalid email or password"):
            login_user(db, "test@example.com", "WrongPassword123!")


def test_login_user_rejects_inactive_account():
    db = MagicMock()

    user = User(
        id=1,
        full_name="Inactive User",
        email="inactive@example.com",
        hashed_password="hashed_password",
        is_active=False,
    )
    db.scalar.return_value = user

    with patch(
        "app.services.auth_service.verify_password",
        return_value=True,
    ):
        with pytest.raises(ValueError, match="User account is inactive"):
            login_user(db, "inactive@example.com", "TestPassword123!")