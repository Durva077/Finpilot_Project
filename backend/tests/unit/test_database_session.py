import pytest

from app.db.session import get_db


def test_get_db_provides_and_closes_session(monkeypatch):
    class DummySession:
        closed = False

        def close(self):
            self.closed = True

    dummy_session = DummySession()

    monkeypatch.setattr(
        "app.db.session.SessionLocal",
        lambda: dummy_session
    )

    db_generator = get_db()

    db = next(db_generator)

    assert db is dummy_session
    assert dummy_session.closed is False

    with pytest.raises(StopIteration):
        next(db_generator)

    assert dummy_session.closed is True
