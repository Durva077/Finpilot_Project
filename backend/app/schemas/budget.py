
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    category_id: int = Field(gt=0)
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)


class BudgetUpdate(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    month: int
    year: int

    model_config = ConfigDict(from_attributes=True)


class BudgetProgressResponse(BudgetResponse):
    spent: Decimal
    remaining: Decimal
    percentage_used: float
    is_exceeded: bool
