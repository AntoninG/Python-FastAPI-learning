from sqlalchemy.orm import Session

from app.repositories import article, user
from tests.main import TestCase, TestingSessionLocal


class TestUserRepository(TestCase):
    db: Session = None

    def setUp(self) -> None:
        super(TestUserRepository, self).setUp()
        self.db = TestingSessionLocal()

    def test_create_user(self):
        pass

    def test_get_user(self):
        pass


class TestArticleRepository(TestCase):
    db: Session = None

    def setUp(self) -> None:
        super(TestArticleRepository, self).setUp()
        self.db = TestingSessionLocal()

    def test_create_article(self):
        pass

    def test_get_article(self):
        pass

    def test_get_all_article(self):
        pass

    def test_update_article(self):
        pass

    def test_delete_article(self):
        pass
