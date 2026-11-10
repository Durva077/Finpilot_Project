from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.schemas.auth import UserRegister, TokenResponse


def register_user(db: Session, user_data: UserRegister) -> User:
    """Register a new user after checking email uniqueness."""

    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if existing_user:
        raise ValueError("Email is already registered")

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, email: str, password: str) -> TokenResponse:
    """Authenticate a user and generate an access token."""

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    return TokenResponse(
        access_token=create_access_token(user.id),
        token_type="bearer",
    )
