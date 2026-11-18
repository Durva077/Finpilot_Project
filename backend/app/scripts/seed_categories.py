
from app.db.session import SessionLocal
from app.services.category_service import seed_default_categories


def main():
    db = SessionLocal()
    try:
        seed_default_categories(db)
        print("Default categories seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
