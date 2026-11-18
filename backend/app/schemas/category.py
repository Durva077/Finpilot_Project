
from pydantic import BaseModel, ConfigDict
from typing import Literal


CategoryType = Literal["income", "expense"]


class CategoryResponse(BaseModel):
    id: int
    name: str
    category_type: CategoryType
    is_default: bool

    model_config = ConfigDict(from_attributes=True)
