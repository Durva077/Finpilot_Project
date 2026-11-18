
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def validate_category(
    db: Session,
    category_id: int,
    user_id: int,
    transaction_type: str | None = None,
) -> Category:
    """Validate category ownership and transaction type."""

    category = db.scalar(
        select(Category).where(
            Category.id == category_id,
            (
                (Category.user_id == user_id)
                | (
                    (Category.user_id.is_(None))
                    & (Category.is_default.is_(True))
                )
            ),
        )
    )

    if category is None:
        raise ValueError("Category not found or unavailable")

    if (
        transaction_type is not None
        and category.category_type != transaction_type
    ):
        raise ValueError("Category type does not match transaction type")

    return category


def create_transaction(
    db: Session,
    user: User,
    transaction_data: TransactionCreate,
) -> Transaction:
    """Create a transaction for the authenticated user."""

    validate_category(
        db,
        transaction_data.category_id,
        user.id,
        transaction_data.transaction_type,
    )

    transaction = Transaction(
        user_id=user.id,
        category_id=transaction_data.category_id,
        amount=transaction_data.amount,
        transaction_type=transaction_data.transaction_type,
        description=transaction_data.description,
        transaction_date=transaction_data.transaction_date,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(
    db: Session,
    user_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    category_id: int | None = None,
    transaction_type: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Transaction]:
    """List transactions belonging to a user with optional filters."""

    query = select(Transaction).where(
        Transaction.user_id == user_id
    )

    if start_date is not None:
        query = query.where(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        query = query.where(
            Transaction.transaction_date <= end_date
        )

    if category_id is not None:
        query = query.where(
            Transaction.category_id == category_id
        )

    if transaction_type is not None:
        query = query.where(
            Transaction.transaction_type == transaction_type
        )

    query = (
        query
        .order_by(Transaction.transaction_date.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(db.scalars(query).all())


def get_transaction_by_id(
    db: Session,
    transaction_id: int,
    user_id: int,
) -> Transaction:
    """Get a transaction only if it belongs to the user."""

    transaction = db.scalar(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
        )
    )

    if transaction is None:
        raise ValueError("Transaction not found")

    return transaction


def update_transaction(
    db: Session,
    transaction_id: int,
    user: User,
    update_data: TransactionUpdate,
) -> Transaction:
    """Update a transaction owned by the authenticated user."""

    transaction = get_transaction_by_id(
        db,
        transaction_id,
        user.id,
    )

    changes = update_data.model_dump(exclude_unset=True)

    new_category_id = changes.get(
        "category_id",
        transaction.category_id,
    )

    new_transaction_type = changes.get(
        "transaction_type",
        transaction.transaction_type,
    )

    validate_category(
        db,
        new_category_id,
        user.id,
        new_transaction_type,
    )

    for field, value in changes.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(
    db: Session,
    transaction_id: int,
    user_id: int,
) -> None:
    """Delete a transaction owned by the user."""

    transaction = get_transaction_by_id(
        db,
        transaction_id,
        user_id,
    )

    db.delete(transaction)
    db.commit()
