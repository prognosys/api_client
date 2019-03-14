from unittest import TestCase
from unittest.mock import Mock, patch
import api_client

TOKEN = 'secret_token'
READING_ENDPOINT = '/readings/'


class TestApiClient(TestCase):

    def setUp(self):
        self.api = api_client.ApiClient(TOKEN)

    @patch('api_client.requests.get')
    def test_get(self, mock_get):
        expected = {
            'reading': 'ok'
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected
        
        response = self.api.get(READING_ENDPOINT)

        self.assertIsNotNone(response)
        self.assertDictEqual(response, expected)

    @patch('api_client.requests.get')
    def test_get_invalid(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = 'Server error'

        self.assertRaises(api_client.HttpError, self.api.get, READING_ENDPOINT)
        
    @patch('api_client.requests.post')
    def test_post(self, mock_post):
        expected = {
            'reading': 'post'
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = expected

        response = self.api.post(READING_ENDPOINT, expected)

        self.assertIsNotNone(response)
        self.assertDictEqual(response, expected)

        mock_post.return_value.status_code = 201

        response = self.api.post(READING_ENDPOINT, expected)

        self.assertIsNotNone(response)
        self.assertDictEqual(response, expected)

    @patch('api_client.requests.post')
    def test_post_invalid(self, mock_post):
        expected = {'reading': 'post'}
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = 'Server error'

        self.assertRaises(api_client.HttpError, self.api.post, READING_ENDPOINT, expected)