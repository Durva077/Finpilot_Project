from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.dashboard import DashboardSummary, CategorySpending


def get_dashboard_summary(
    db: Session,
    user: User,
) -> DashboardSummary:
    """Calculate dashboard figures for the authenticated user."""

    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    if now.month == 12:
        next_month = month_start.replace(
            year=now.year + 1,
            month=1,
        )
    else:
        next_month = month_start.replace(
            month=now.month + 1,
        )

    # Calculate lifetime income and expenses.
    totals_query = select(
        func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.transaction_type == "income",
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("total_income"),
        func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.transaction_type == "expense",
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("total_expenses"),
    ).where(Transaction.user_id == user.id)

    totals = db.execute(totals_query).one()

    total_income = Decimal(str(totals.total_income))
    total_expenses = Decimal(str(totals.total_expenses))
    starting_balance = Decimal(str(user.starting_balance))

    current_balance = (
        starting_balance + total_income - total_expenses
    )

    # Calculate current month's income and expenses.
    monthly_query = select(
        func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.transaction_type == "income",
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("monthly_income"),
        func.coalesce(
            func.sum(
                case(
                    (
                        Transaction.transaction_type == "expense",
                        Transaction.amount,
                    ),
                    else_=0,
                )
            ),
            0,
        ).label("monthly_expenses"),
    ).where(
        Transaction.user_id == user.id,
        Transaction.transaction_date >= month_start,
        Transaction.transaction_date < next_month,
    )

    monthly = db.execute(monthly_query).one()

    monthly_income = Decimal(str(monthly.monthly_income))
    monthly_expenses = Decimal(str(monthly.monthly_expenses))

    monthly_savings = monthly_income - monthly_expenses

    # Calculate current month's expense by category.
    category_query = (
        select(
            Category.id,
            Category.name,
            func.sum(Transaction.amount).label("total_amount"),
        )
        .join(
            Transaction,
            Transaction.category_id == Category.id,
        )
        .where(
            Transaction.user_id == user.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= month_start,
            Transaction.transaction_date < next_month,
        )
        .group_by(Category.id, Category.name)
        .order_by(func.sum(Transaction.amount).desc())
    )

    category_results = db.execute(category_query).all()

    category_spending = [
        CategorySpending(
            category_id=row.id,
            category_name=row.name,
            total_amount=row.total_amount,
        )
        for row in category_results
    ]

    return DashboardSummary(
        starting_balance=starting_balance,
        current_balance=current_balance,
        total_income=total_income,
        total_expenses=total_expenses,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_savings=monthly_savings,
        category_spending=category_spending,
    )