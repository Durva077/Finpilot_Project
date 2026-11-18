
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


DEFAULT_CATEGORIES = [
    ("Salary", "income"),
    ("Freelance", "income"),
    ("Business", "income"),
    ("Investment", "income"),
    ("Other Income", "income"),
    ("Food", "expense"),
    ("Transport", "expense"),
    ("Shopping", "expense"),
    ("Bills", "expense"),
    ("Rent", "expense"),
    ("Healthcare", "expense"),
    ("Entertainment", "expense"),
    ("Education", "expense"),
    ("Travel", "expense"),
    ("Other Expense", "expense"),
]


def seed_default_categories(db: Session) -> None:
    """Create missing shared default categories without duplicates."""

    existing = db.execute(
        select(Category.name, Category.category_type).where(
            Category.user_id.is_(None),
            Category.is_default.is_(True),
        )
    ).all()

    existing_set = set(existing)

    for name, category_type in DEFAULT_CATEGORIES:
        if (name, category_type) not in existing_set:
            db.add(
                Category(
                    user_id=None,
                    name=name,
                    category_type=category_type,
                    is_default=True,
                )
            )

    db.commit()


def get_categories(
    db: Session,
    user_id: int,
    category_type: str | None = None,
) -> list[Category]:
    """Return shared defaults and categories owned by the user."""

    query = select(Category).where(
        (
            (Category.user_id.is_(None))
            & (Category.is_default.is_(True))
        )
        | (Category.user_id == user_id)
    )

    if category_type is not None:
        query = query.where(
            Category.category_type == category_type
        )

    query = query.order_by(
        Category.category_type,
        Category.name,
    )

    return list(db.scalars(query).all())
