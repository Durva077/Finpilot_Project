
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.category import CategoryResponse
from app.services.category_service import get_categories

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    category_type: Literal["income", "expense"] | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List default categories and categories owned by the current user."""
    return get_categories(
        db=db,
        user_id=current_user.id,
        category_type=category_type,
    )
