from fastapi import HTTPException

from app.exceptions.http_exceptions import CredentialsException
from app.models.user import User
from app.repositories import user
from app.schemas.requests import TokenData
from app.utils.token import create_access_token, verify_token
from tests.main import TestCase


class TestCreateAccessToken(TestCase):
    user: User | None = None

    def setUp(self) -> None:
        super(TestCreateAccessToken, self).setUp()

        self.user = user.create(self.db, {
            "name": "Antonin GUILET-DUPONT",
            "email": "antonin@iconosqua.re",
            "password": "password"
        })

    def test_create_access_token(self):
        assert isinstance(create_access_token({
            'id': self.user.id,
            'name': self.user.name,
            'username': self.user.email
        }), str)

    def test_create_access_token_accepts_only_dict(self):
        with self.assertRaises(AttributeError):
            create_access_token('token')

        with self.assertRaises(AttributeError):
            create_access_token(12345)


class TestVerifyToken(TestCase):
    user: User | None
    access_token: str | None

    def setUp(self) -> None:
        super(TestVerifyToken, self).setUp()

        self.user = user.create(self.db, {
            "name": "Antonin GUILET-DUPONT",
            "email": "antonin@iconosqua.re",
            "password": "password"
        })

        self.access_token = create_access_token({
            'id': self.user.id,
            'name': self.user.name,
            'username': self.user.email
        })

    def test_verify_access_token(self):
        credentials_exception = Exception()
        token_data = verify_token(self.access_token, credentials_exception)
        assert isinstance(token_data, TokenData)

        assert token_data.id == self.user.id
        assert token_data.name == self.user.name
        assert token_data.username == self.user.email

    def test_verify_access_token_raises_exception_if_username_missing(self):
        credentials_exception = Exception()
        access_token = create_access_token({
            'id': self.user.id,
            'name': self.user.name
        })

        with self.assertRaises(Exception):
            verify_token(access_token, credentials_exception)

    def test_verify_access_token_accepts_only_str_and_exception(self):
        with self.assertRaises(TypeError):
            verify_token('token', 1)

        with self.assertRaises(TypeError):
            verify_token('token', 'str')

        with self.assertRaises(AttributeError):
            verify_token(1, Exception())

        with self.assertRaises(AttributeError):
            verify_token({}, Exception())

    def test_verify_access_token_accepts_any_exception(self):
        access_token = create_access_token({
            'id': self.user.id,
            'name': self.user.name
        })

        with self.assertRaises(HTTPException):
            verify_token(access_token, HTTPException(status_code=401))

        with self.assertRaises(HTTPException):
            verify_token(access_token, CredentialsException())
