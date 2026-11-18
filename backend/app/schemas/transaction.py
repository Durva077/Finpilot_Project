
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TransactionType = Literal["income", "expense"]


class TransactionCreate(BaseModel):
    category_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_type: TransactionType
    description: str | None = Field(default=None, max_length=1000)
    transaction_date: datetime



class TransactionUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    transaction_type: TransactionType | None = None
    description: str | None = Field(default=None, max_length=1000)
    transaction_date: datetime | None = None

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        required_fields = {
            "category_id",
            "amount",
            "transaction_type",
            "transaction_date",
        }

        for field in required_fields:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")

        return self



class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    transaction_type: str
    description: str | None
    transaction_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
