from sqlalchemy import inspect

from app.db.session import engine

def test_database_contains_all_core_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = {
        "users",
        "categories",
        "transactions",
        "budgets",
    }

    assert expected_tables.issubset(set(tables))