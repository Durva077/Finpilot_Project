from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)


# Create a reusable database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Provide a database session to API endpoints.
    Close the session after the request is completed.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
