
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.budget import (
    BudgetCreate,
    BudgetProgressResponse,
    BudgetResponse,
    BudgetUpdate,
)


def validate_expense_category(
    db: Session,
    category_id: int,
    user_id: int,
) -> Category:
    category = db.scalar(
        select(Category).where(
            Category.id == category_id,
            (
                (Category.user_id == user_id)
                | (
                    Category.user_id.is_(None)
                    & (Category.is_default.is_(True))
                )
            ),
        )
    )

    if category is None:
        raise ValueError("Category not found or unavailable")

    # Adjust this check if your Category model uses a different field name.
    if category.category_type != "expense":
        raise ValueError("Budgets can only be created for expense categories")

    return category


def get_budget_or_raise(
    db: Session,
    budget_id: int,
    user_id: int,
) -> Budget:
    budget = db.scalar(
        select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )
    )

    if budget is None:
        raise ValueError("Budget not found")

    return budget


def calculate_budget_progress(
    db: Session,
    budget: Budget,
    user_id: int,
) -> BudgetProgressResponse:
    spent = db.scalar(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.category_id == budget.category_id,
            Transaction.transaction_type == "expense",
            extract("month", Transaction.transaction_date) == budget.month,
            extract("year", Transaction.transaction_date) == budget.year,
        )
    )

    spent = Decimal(str(spent or 0))
    remaining = budget.amount - spent

    return BudgetProgressResponse(
        **BudgetResponse.model_validate(budget).model_dump(),
        spent=spent,
        remaining=remaining,
        percentage_used=round(float(spent / budget.amount * 100), 2),
        is_exceeded=spent > budget.amount,
    )


def create_budget(
    db: Session,
    budget_data: BudgetCreate,
    user_id: int,
) -> Budget:
    validate_expense_category(db, budget_data.category_id, user_id)

    existing = db.scalar(
        select(Budget).where(
            Budget.user_id == user_id,
            Budget.category_id == budget_data.category_id,
            Budget.month == budget_data.month,
            Budget.year == budget_data.year,
        )
    )

    if existing:
        raise ValueError("A budget already exists for this category and period")

    budget = Budget(
        user_id=user_id,
        category_id=budget_data.category_id,
        amount=budget_data.amount,
        month=budget_data.month,
        year=budget_data.year,
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def list_budgets(
    db: Session,
    user_id: int,
    month: int | None = None,
    year: int | None = None,
) -> list[BudgetProgressResponse]:
    query = select(Budget).where(Budget.user_id == user_id)

    if month is not None:
        query = query.where(Budget.month == month)

    if year is not None:
        query = query.where(Budget.year == year)

    budgets = db.scalars(
        query.order_by(Budget.year.desc(), Budget.month.desc())
    ).all()

    return [
        calculate_budget_progress(db, budget, user_id)
        for budget in budgets
    ]


def get_budget(
    db: Session,
    budget_id: int,
    user_id: int,
) -> BudgetProgressResponse:
    budget = get_budget_or_raise(db, budget_id, user_id)
    return calculate_budget_progress(db, budget, user_id)


def update_budget(
    db: Session,
    budget_id: int,
    budget_data: BudgetUpdate,
    user_id: int,
) -> Budget:
    budget = get_budget_or_raise(db, budget_id, user_id)

    budget.amount = budget_data.amount

    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(
    db: Session,
    budget_id: int,
    user_id: int,
) -> None:
    budget = get_budget_or_raise(db, budget_id, user_id)

    db.delete(budget)
    db.commit()
