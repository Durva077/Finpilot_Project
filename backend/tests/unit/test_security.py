import jwt

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def test_hash_password_does_not_store_plain_text():
    password = "TestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("CorrectPassword123!")

    assert verify_password("WrongPassword123!", hashed) is False


def test_create_access_token_contains_user_id():
    token = create_access_token(user_id=1)

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    assert payload["sub"] == "1"
    assert "exp" in payload