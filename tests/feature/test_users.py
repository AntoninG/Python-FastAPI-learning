from app.repositories import article, user
from tests.main import TestCase, client


class TestPostUser(TestCase):
    endpoint = '/users/'

    def test_create_user_accepts_only_post(self):
        assert client.get(self.endpoint).status_code == 405
        assert client.put(self.endpoint).status_code == 405
        assert client.patch(self.endpoint).status_code == 405
        assert client.delete(self.endpoint).status_code == 405
        assert client.head(self.endpoint).status_code == 405
        assert client.post(self.endpoint).status_code == 422

    def test_create_user_correctly(self):
        response = client.post(
            self.endpoint,
            json={
                'name': 'Antonin',
                'email': 'antonin@iconosqua.re',
                'password': 'dev3387V!DEO'
            }
        )

        assert response.status_code == 201
        self.assertDictEqual(response.json(), {
            'id': 1,
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re'
        })

    def test_create_user_email_exists_already(self):
        assert client.post(
            self.endpoint,
            json={
                'name': 'Antonin',
                'email': 'antonin@iconosqua.re',
                'password': 'dev3387V!DEO'
            }
        ).status_code == 201

        assert client.post(
            self.endpoint,
            json={
                'name': 'Antoin',
                'email': 'antonin@iconosqua.re',
                'password': 'dev3387V!DEO'
            }
        ).status_code == 304

    def test_create_user_with_too_much_information(self):
        response = client.post(
            self.endpoint,
            json={
                'name': 'Antonin',
                'email': 'antonin@iconosqua.re',
                'password': 'dev3387V!DEO',
                'settings': {},
                'foo': 'bar'
            }
        )

        assert response.status_code == 201
        self.assertDictEqual(response.json(), {
            'id': 1,
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re'
        })

    def test_create_user_invalid_email(self):
        response = client.post(
            self.endpoint,
            json={
                'name': 'Antonin',
                'email': 'antonin@t',
                'password': 'dev3387V!DEO'
            }
        )

        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'loc': ['body', 'email'],
                    'msg': 'value is not a valid email address',
                    'type': 'value_error.email'
                }
            ]
        }

    def test_create_user_invalid_password(self):
        response = client.post(
            self.endpoint,
            json={
                'name': 'Antonin',
                'email': 'antonin@iconosqua.re',
                'password': 'password',
            }
        )

        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'loc': ['body', 'password'],
                    'msg': 'must be a valid password (8 to 30 chars, with '
                           'digits, upper and lower case, symbols and no spaces)',
                    'type': 'value_error'
                }
            ]
        }

    def test_create_user_missing_data(self):
        response = client.post(self.endpoint, json={})

        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'loc': ['body', 'name'],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                },
                {
                    'loc': ['body', 'email'],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                },
                {
                    'loc': ['body', 'password'],
                    'msg': 'field required',
                    'type': 'value_error.missing'
                },
            ]
        }


class TestGetUser(TestCase):
    endpoint = '/users/{0}'

    def test_get_user_accepts_only_get(self):
        assert client.put(self.endpoint.format(1)).status_code == 405
        assert client.patch(self.endpoint.format(1)).status_code == 405
        assert client.delete(self.endpoint.format(1)).status_code == 405
        assert client.head(self.endpoint.format(1)).status_code == 405
        assert client.post(self.endpoint.format(1)).status_code == 405

    def test_get_user_does_not_exist(self):
        response = client.get(self.endpoint.format(1))
        assert response.status_code == 404
        assert response.json() == {
            'detail': 'Not Found'
        }

    def test_get_user_without_articles(self):
        user.create(self.db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO',
        })

        response = client.get(self.endpoint.format(1))
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'articles': []
        }

    def test_get_user_with_articles(self):
        user.create(self.db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO',
        })
        article.create(db, {'title': 'Article', 'content': 'Body'})

        response = client.get(self.endpoint.format(1))
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'articles': [
                {'id': 1, 'title': 'Article', 'content': 'Body'}
            ]
        }
