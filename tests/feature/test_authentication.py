from app.models.user import User
from app.repositories import user
from app.utils.token import create_access_token
from tests.main import TestCase, client


class TestLoginRoute(TestCase):
    user: User | None
    endpoint: str = "/login"

    def setUp(self) -> None:
        super(TestLoginRoute, self).setUp()

        self.user = user.create(self.db, {
            "name": "Antonin GUILET-DUPONT",
            "email": "antonin@iconosqua.re",
            "password": "password"
        })

    def test_login_unprocessable_request(self):
        assert client.post(self.endpoint, data={
            "grant_type": "password",
            "password": "password",
            "email": "antonin@iconosqua.re",
        }).status_code == 422

        assert client.post(self.endpoint, data={
            "grant_type": "password",
            "motdepasse": "password",
            "username": "antonin@iconosqua.re"
        }).status_code == 422

    def test_login_non_existing_user(self):
        response = client.post(
            self.endpoint,
            data={
                "grant_type": "password",
                "password": "password",
                "username": "antonin@iconosquare.com"
            }
        )

        assert response.status_code == 401

    def test_login_wrong_password(self):
        response = client.post(self.endpoint, data={
            "grant_type": "password",
            "password": "dev3387V!DEO",
            "username": "antonin@iconosquare.com"
        })

        assert response.status_code == 401

    def test_login_success(self):
        response = client.post(self.endpoint, data={
            "grant_type": "password",
            "username": "antonin@iconosqua.re",
            "password": "password"
        })

        assert response.status_code == 200

        json = response.json()
        assert "access_token" in json
        assert json["token_type"] == "bearer"

class TestSlashMeRoute(TestCase):
    user: User | None
    access_token: str | None
    endpoint: str = "/me"

    def setUp(self) -> None:
        super(TestSlashMeRoute, self).setUp()

        self.user = user.create(self.db, {
            "name": "Antonin GUILET-DUPONT",
            "email": "antonin@iconosqua.re",
            "password": "password"
        })

        self.access_token = create_access_token({
            "id": self.user.id,
            "name": self.user.name,
            "username": self.user.email
        })

    def test_unauthorized(self):
        assert client.get(self.endpoint).status_code == 401
        assert client.get(
            self.endpoint,
            headers={"Authorization": "Bearer foobarbaz12345"}
        ).status_code == 401

    def test_success(self):
        response = client.get(
            self.endpoint,
            headers={"Authorization": "Bearer " + self.access_token}
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Antonin GUILET-DUPONT",
            "email": "antonin@iconosqua.re",
            "password": "**********",
            "articles": []
        }
