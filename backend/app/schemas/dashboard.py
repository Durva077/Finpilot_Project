from decimal import Decimal
from pydantic import BaseModel


class CategorySpending(BaseModel):
    category_id: int
    category_name: str
    total_amount: Decimal


class DashboardSummary(BaseModel):
    starting_balance: Decimal
    current_balance: Decimal

    total_income: Decimal
    total_expenses: Decimal

    monthly_income: Decimal
    monthly_expenses: Decimal
    monthly_savings: Decimal

    category_spending: list[CategorySpending]