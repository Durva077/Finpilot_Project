
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.budget import (
    BudgetCreate,
    BudgetProgressResponse,
    BudgetResponse,
    BudgetUpdate,
)
from app.services.budget_service import (
    create_budget,
    list_budgets,
    get_budget,
    update_budget,
    delete_budget,
)

router = APIRouter(
    prefix="/api/budgets",
    tags=["Budgets"],
)


@router.post(
    "",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_budget_endpoint(
    budget_data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_budget(db, budget_data, current_user.id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get("", response_model=list[BudgetProgressResponse])
def list_budgets_endpoint(
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = Query(default=None, ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_budgets(db, current_user.id, month, year)


@router.get("/{budget_id}", response_model=BudgetProgressResponse)
def retrieve_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_budget(db, budget_id, current_user.id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.put("/{budget_id}", response_model=BudgetResponse)
def edit_budget(
    budget_id: int,
    update_data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_budget(db, budget_id, update_data, current_user.id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_budget(db, budget_id, current_user.id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
