import contextlib
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.utils.database as database
from app.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

database.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestCase(unittest.TestCase):
    refresh_database: bool = True
    db: Session | None

    def setUp(self) -> None:
        self.db = TestingSessionLocal()

    def tearDown(self) -> None:
        if self.refresh_database is True:
            with contextlib.closing(engine.connect()) as con:
                trans = con.begin()
                for table in reversed(database.Base.metadata.sorted_tables):
                    con.execute(table.delete())
                trans.commit()
