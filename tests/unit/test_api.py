from tests.main import TestCase, client


class TestApi(TestCase):
    def test_api_answers(self):
        response = client.get('/about')
        assert response.status_code == 200

        json = response.json()
        assert 'project' in json
        assert 'created' in json
        assert 'author' in json

    def test_api_page_not_found(self):
        response = client.get('/random')
        assert response.status_code == 404
        assert response.json() == {'detail': 'Not Found'}

    def test_api_wrong_method(self):
        response = client.put('/about')
        assert response.status_code == 405
        assert response.json() == {'detail': 'Method Not Allowed'}
