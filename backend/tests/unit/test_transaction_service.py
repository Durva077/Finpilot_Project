
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services import transaction_service


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def test_user():
    return SimpleNamespace(id=1)


@pytest.fixture
def test_category():
    return SimpleNamespace(
        id=10,
        user_id=None,
        category_type="expense",
        is_default=True,
    )


@pytest.fixture
def test_transaction():
    return SimpleNamespace(
        id=100,
        user_id=1,
        category_id=10,
        amount=Decimal("500.00"),
        transaction_type="expense",
        description="Test transaction",
        transaction_date=datetime(
            2026, 11, 18, 10, 0, tzinfo=timezone.utc
        ),
    )


@pytest.fixture
def transaction_create_data():
    return TransactionCreate(
        category_id=10,
        amount=Decimal("500.00"),
        transaction_type="expense",
        description="Test transaction",
        transaction_date=datetime(
            2026, 11, 18, 10, 0, tzinfo=timezone.utc
        ),
    )


# -----------------------------
# CATEGORY VALIDATION UNIT TESTS
# -----------------------------

def test_validate_category_success(mock_db, test_category):
    mock_db.scalar.return_value = test_category

    result = transaction_service.validate_category(
        mock_db,
        category_id=10,
        user_id=1,
        transaction_type="expense",
    )

    assert result == test_category
    mock_db.scalar.assert_called_once()


def test_validate_category_not_found(mock_db):
    mock_db.scalar.return_value = None

    with pytest.raises(ValueError, match="Category not found"):
        transaction_service.validate_category(
            mock_db,
            category_id=999,
            user_id=1,
        )


def test_validate_category_type_mismatch(mock_db, test_category):
    mock_db.scalar.return_value = test_category

    with pytest.raises(ValueError, match="Category type"):
        transaction_service.validate_category(
            mock_db,
            category_id=10,
            user_id=1,
            transaction_type="income",
        )


# -----------------------------
# CREATE TRANSACTION UNIT TEST
# -----------------------------

@patch("app.services.transaction_service.validate_category")
def test_create_transaction_success(
    mock_validate_category,
    mock_db,
    test_user,
    transaction_create_data,
):
    result = transaction_service.create_transaction(
        mock_db,
        test_user,
        transaction_create_data,
    )

    assert isinstance(result, Transaction)
    assert result.user_id == test_user.id
    assert result.category_id == 10
    assert result.amount == Decimal("500.00")
    assert result.transaction_type == "expense"

    mock_validate_category.assert_called_once()
    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)


# -----------------------------
# GET TRANSACTIONS UNIT TESTS
# -----------------------------

def test_get_transactions_returns_list(mock_db):
    expected_transactions = [
        SimpleNamespace(id=1),
        SimpleNamespace(id=2),
    ]

    mock_db.scalars.return_value.all.return_value = expected_transactions

    result = transaction_service.get_transactions(
        mock_db,
        user_id=1,
    )

    assert result == expected_transactions
    mock_db.scalars.assert_called_once()


def test_get_transactions_returns_empty_list(mock_db):
    mock_db.scalars.return_value.all.return_value = []

    result = transaction_service.get_transactions(
        mock_db,
        user_id=1,
    )

    assert result == []


def test_get_transactions_with_filters(mock_db):
    mock_db.scalars.return_value.all.return_value = []

    start_date = datetime(
        2026, 11, 1, tzinfo=timezone.utc
    )
    end_date = datetime(
        2026, 11, 30, tzinfo=timezone.utc
    )

    result = transaction_service.get_transactions(
        mock_db,
        user_id=1,
        start_date=start_date,
        end_date=end_date,
        category_id=10,
        transaction_type="expense",
        limit=20,
        offset=5,
    )

    assert result == []
    mock_db.scalars.assert_called_once()


# -----------------------------
# GET TRANSACTION BY ID TESTS
# -----------------------------

def test_get_transaction_by_id_success(
    mock_db,
    test_transaction,
):
    mock_db.scalar.return_value = test_transaction

    result = transaction_service.get_transaction_by_id(
        mock_db,
        transaction_id=100,
        user_id=1,
    )

    assert result == test_transaction
    mock_db.scalar.assert_called_once()


def test_get_transaction_by_id_not_found(mock_db):
    mock_db.scalar.return_value = None

    with pytest.raises(ValueError, match="Transaction not found"):
        transaction_service.get_transaction_by_id(
            mock_db,
            transaction_id=999,
            user_id=1,
        )


# -----------------------------
# UPDATE TRANSACTION UNIT TESTS
# -----------------------------

@patch("app.services.transaction_service.validate_category")
@patch("app.services.transaction_service.get_transaction_by_id")
def test_update_transaction_success(
    mock_get_transaction,
    mock_validate_category,
    mock_db,
    test_user,
    test_transaction,
):
    mock_get_transaction.return_value = test_transaction

    update_data = TransactionUpdate(
        amount=Decimal("750.00"),
        description="Updated transaction",
    )

    result = transaction_service.update_transaction(
        mock_db,
        transaction_id=100,
        user=test_user,
        update_data=update_data,
    )

    assert result.amount == Decimal("750.00")
    assert result.description == "Updated transaction"

    mock_get_transaction.assert_called_once_with(
        mock_db,
        100,
        test_user.id,
    )
    mock_validate_category.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(test_transaction)


@patch("app.services.transaction_service.get_transaction_by_id")
def test_update_transaction_not_found(
    mock_get_transaction,
    mock_db,
    test_user,
):
    mock_get_transaction.side_effect = ValueError(
        "Transaction not found"
    )

    update_data = TransactionUpdate(
        amount=Decimal("750.00")
    )

    with pytest.raises(ValueError, match="Transaction not found"):
        transaction_service.update_transaction(
            mock_db,
            transaction_id=999,
            user=test_user,
            update_data=update_data,
        )

    mock_db.commit.assert_not_called()


# -----------------------------
# DELETE TRANSACTION UNIT TESTS
# -----------------------------

@patch("app.services.transaction_service.get_transaction_by_id")
def test_delete_transaction_success(
    mock_get_transaction,
    mock_db,
    test_transaction,
):
    mock_get_transaction.return_value = test_transaction

    result = transaction_service.delete_transaction(
        mock_db,
        transaction_id=100,
        user_id=1,
    )

    assert result is None
    mock_get_transaction.assert_called_once_with(
        mock_db,
        100,
        1,
    )
    mock_db.delete.assert_called_once_with(test_transaction)
    mock_db.commit.assert_called_once()


@patch("app.services.transaction_service.get_transaction_by_id")
def test_delete_transaction_not_found(
    mock_get_transaction,
    mock_db,
):
    mock_get_transaction.side_effect = ValueError(
        "Transaction not found"
    )

    with pytest.raises(ValueError, match="Transaction not found"):
        transaction_service.delete_transaction(
            mock_db,
            transaction_id=999,
            user_id=1,
        )

    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()
