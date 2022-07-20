from app.repositories import user
from tests.main import TestCase, TestingSessionLocal, client


class TestPassword(TestCase):
    endpoint = '/users/verify-password?email={0}'

    def setUp(self) -> None:
        super(TestPassword, self).setUp()

        db = TestingSessionLocal()
        user.create(db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO'
        })

    def test_verifies_password_non_existing_user(self):
        response = client.post(
            self.endpoint.format('antonin@iconosquare.com'),
            json={'password': 'dev3387V!DEO'}
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'Unauthorized'}

    def test_verifies_password_wrong_password(self):
        response = client.post(
            self.endpoint.format('antonin@iconosqua.re'),
            json={'password': 'password'}
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'Unauthorized'}

    def test_verifies_password_true_password(self):
        response = client.post(
            self.endpoint.format('antonin@iconosqua.re'),
            json={'password': 'dev3387V!DEO'}
        )

        assert response.status_code == 200
        assert response.json() is True

    def test_missing_email_param(self):
        response = client.post(
            '/users/verify-password?param=1',
            json={'password': 'dev3387V!DEO'}
        )

        assert response.status_code == 422
