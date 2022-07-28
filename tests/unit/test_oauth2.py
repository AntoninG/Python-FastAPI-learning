from sqlalchemy.orm import Session

from app.exceptions.http_exceptions import CredentialsException
from app.models.user import User
from app.repositories import user
from app.utils.oauth2 import current_user
from app.utils.token import create_access_token
from tests.main import TestCase


class TestCurrentUser(TestCase):
    user: User | None

    def setUp(self) -> None:
        super(TestCurrentUser, self).setUp()

        self.user = user.create(self.db, {
            "name": "Antonin GUILET-DUPONT",
            "email": "antonin@iconosqua.re",
            "password": "password"
        })

    def test_current_user_raises_credentials_exception(self):
        with self.assertRaises(CredentialsException):
            access_token = create_access_token({
                'id': self.user.id,
                'name': self.user.name,
            })
            current_user(access_token, self.db)

    def test_current_user_returns_user(self):
        access_token = create_access_token({
            'id': self.user.id,
            'name': self.user.name,
            'username': self.user.email
        })
        user_got = current_user(access_token, self.db)
        assert user_got.id == self.user.id
