from app.repositories import article, user
from tests.main import TestCase, client


class TestIndexArticles(TestCase):
    endpoint = '/articles/'

    def setUp(self) -> None:
        super(TestIndexArticles, self).setUp()

        user.create(self.db, {
            'name': 'A',
            'email': 'email@mail.com',
            'password': 'dev3387V!DEO'
        })

    def create_article(self, dictionary: dict |None = None):
        if dictionary is None:
            dictionary = {'title': 'Title', 'content': 'Content'}

        article.create(self.db, dictionary)

    def test_index_accepts_only_get(self):
        assert client.get(self.endpoint).status_code == 200
        assert client.post(self.endpoint).status_code == 422
        assert client.put(self.endpoint).status_code == 405
        assert client.patch(self.endpoint).status_code == 405
        assert client.delete(self.endpoint).status_code == 405
        assert client.head(self.endpoint).status_code == 405

    def test_index_no_data(self):
        response = client.get(self.endpoint)
        assert response.status_code == 200
        assert response.json() == []

    def test_index_one_article(self):
        self.create_article()

        response = client.get(self.endpoint)
        assert response.status_code == 200

        json = response.json()
        assert len(json) == 1
        assert json[0] == {
            'id': 1,
            'title': 'Title',
            'content': 'Content',
            'author': {
                'id': 1,
                'name': 'A',
                'email': 'email@mail.com'
            }
        }

    def test_index_two_articles(self):
        db = self.db
        self.create_article({'title': 'Titre', 'content': 'Content'})

        user.create(db, {'name': 'B', 'email': 'mail@email.com', 'password': 'pwd'})
        self.create_article({'title': 'Title', 'content': 'Contenu', 'user_id': 2})

        response = client.get(self.endpoint, params={'limit': None})
        assert response.status_code == 200

        json = response.json()
        assert len(json) == 2
        assert json[0] == {
            'id': 1,
            'title': 'Titre',
            'content': 'Content',
            'author': {
                'id': 1,
                'name': 'A',
                'email': 'email@mail.com'
            }
        }
        assert json[1] == {
            'id': 2,
            'title': 'Title',
            'content': 'Contenu',
            'author': {
                'id': 2,
                'name': 'B',
                'email': 'mail@email.com'
            }
        }

    def test_limit_param(self):
        self.create_article()

        assert len(client.get(self.endpoint, params={'limit': 0}).json()) == 0
        assert len(client.get(self.endpoint, params={'limit': 1}).json()) == 1
        assert len(client.get(self.endpoint, params={'limit': 10}).json()) == 1
        assert len(client.get(self.endpoint, params={'limit': None}).json()) == 1

    def test_offset_param(self):
        self.create_article()

        assert len(
            client.get(self.endpoint, params={'limit': None, 'offset': 0}).json()) == 1
        assert len(
            client.get(self.endpoint, params={'limit': None, 'offset': 1}).json()) == 0
        assert len(
            client.get(self.endpoint, params={'limit': None, 'offset': 10}).json()) == 0

    def test_query_param(self):
        self.create_article()

        assert len(
            client.get(self.endpoint, params={'query': None}).json()) == 1
        assert len(
            client.get(self.endpoint, params={'query': 'Title'}).json()) == 1
        assert len(
            client.get(self.endpoint, params={'query': 'Ti'}).json()) == 1
        assert len(
            client.get(self.endpoint, params={'query': 'tle'}).json()) == 1
        assert len(
            client.get(self.endpoint, params={'query': 'ti'}).json()) == 1
        assert len(
            client.get(self.endpoint, params={'query': 'Content'}).json()) == 0


class TestGetArticle(TestCase):
    endpoint = '/articles/{0}'

    def setUp(self) -> None:
        super(TestGetArticle, self).setUp()

        user.create(self.db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO'
        })

        article.create(self.db, {'title': 'Title', 'content': 'Content'})

    def test_get_non_existing_article(self):
        assert client.get(self.endpoint.format(2)).status_code == 404

    def test_get_existing_article(self):
        response = client.get(self.endpoint.format(1))
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'title': 'Title',
            'content': 'Content',
            'author': {
                'id': 1,
                'name': 'Antonin',
                'email': 'antonin@iconosqua.re'
            }
        }


class TestCreateArticle(TestCase):
    endpoint = '/articles/'

    def setUp(self) -> None:
        super(TestCreateArticle, self).setUp()

        user.create(self.db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO'
        })

    def test_create_correct_article_without_user(self):
        response = client.post(self.endpoint, json={
            'title': 'Title', 'content': 'Long content'
        })

        assert response.status_code == 201
        assert response.json() == {
            'id': 1,
            'title': 'Title',
            'content': 'Long content'
        }

    def test_create_correct_article_with_user(self):
        new_user = user.create(self.db, {'name': 'A', 'email': 'B', 'password': 'C'})
        response = client.post(self.endpoint, json={
            'title': 'Title', 'content': 'Long content', 'user_id': new_user.id
        })

        assert response.status_code == 201
        assert response.json() == {
            'id': 1,
            'title': 'Title',
            'content': 'Long content'
        }

    def test_create_incorrect_article(self):
        response = client.post(self.endpoint, json={
            'title': 'T', 'content': 'L'
        })

        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'ctx': {'limit_value': 2},
                    'loc': ['body', 'title'],
                    'msg': 'ensure this value has at least 2 characters',
                    'type': 'value_error.any_str.min_length'
                },
                {
                    'ctx': {'limit_value': 10},
                    'loc': ['body', 'content'],
                    'msg': 'ensure this value has at least 10 characters',
                    'type': 'value_error.any_str.min_length'
                }
            ]
        }


class TestUpdateArticle(TestCase):
    endpoint = '/articles/{0}'

    def setUp(self) -> None:
        super(TestUpdateArticle, self).setUp()

        user.create(self.db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO'
        })
        self.article = article.create(self.db, {
            'title': 'Article title',
            'content': 'Content of the article'
        })

    def test_update_article(self):
        response = client.put(self.endpoint.format(self.article.id), json={
            'title': 'Article title 2',
            'content': 'Content of the article 2'
        })

        assert response.status_code == 202
        assert response.json() == {
            'id': 1,
            'title': 'Article title 2',
            'content': 'Content of the article 2'
        }

    def test_update_incorrect_article(self):
        response = client.put(self.endpoint.format(self.article.id), json={
            'title': 'A',
            'content': 'Content'
        })

        assert response.status_code == 422
        assert response.json() == {
            'detail': [
                {
                    'ctx': {'limit_value': 2},
                    'loc': ['body', 'title'],
                    'msg': 'ensure this value has at least 2 characters',
                    'type': 'value_error.any_str.min_length'
                },
                {
                    'ctx': {'limit_value': 10},
                    'loc': ['body', 'content'],
                    'msg': 'ensure this value has at least 10 characters',
                    'type': 'value_error.any_str.min_length'
                }
            ]
        }

    def test_update_non_existing_article(self):
        assert client.put(self.endpoint.format(2), json={
            'title': 'Article title',
            'content': 'Content of the article'
        }).status_code == 404


class TestDeleteArticle(TestCase):
    endpoint = '/articles/{0}'

    def setUp(self) -> None:
        super(TestDeleteArticle, self).setUp()

        user.create(self.db, {
            'name': 'Antonin',
            'email': 'antonin@iconosqua.re',
            'password': 'dev3387V!DEO'
        })
        self.article = article.create(self.db, {
            'title': 'Article title',
            'content': 'Content of the article'
        })

    def test_delete_existing_article(self):
        assert client.delete(self.endpoint.format(self.article.id)).status_code == 204

    def test_delete_non_existing_article(self):
        assert client.delete(
            self.endpoint.format(2)).status_code == 404