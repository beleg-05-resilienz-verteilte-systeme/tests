import unittest
from . import main
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from requests.exceptions import RequestException, Timeout, HTTPError

# Create a TestClient instance for the FastAPI app
client = TestClient(main.app)

class TestFallbackStrategy(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(main.app)

    @patch("requests.get")
    def test_get_data_success(self, mock_get: MagicMock):
        """Test when the external service returns data successfully."""
        mock_response = {
            "items": [
                {"title": "Test Title 1", "author": "Test Author 1", "year": 2021},
                {"title": "Test Title 2", "author": "Test Author 2", "year": 2022},
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = client.get("/get-data/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["data"], mock_response)

    @patch("requests.get")
    def test_get_data_fallback(self, mock_get: MagicMock):
        """Test when the external service fails and fallback data is used."""
        mock_get.side_effect = RequestException("Service unavailable")

        response = client.get("/get-data/")
        self.assertEqual(response.status_code, 200)  # Still 200 since fallback data is provided
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["data"], main.FALLBACK_DATA)

    @patch("requests.get")
    def test_get_data_timeout(self, mock_get):
        """Test when the external service times out."""
        mock_get.side_effect = Timeout("Timeout error")

        response = client.get("/get-data/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["data"], main.FALLBACK_DATA)

    @patch("requests.get")
    def test_get_data_service_error(self, mock_get: MagicMock):
        """Test when the external service returns an error response."""
        mock_get.side_effect = HTTPError("Internal Server Error")

        response = client.get("/get-data/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["data"], main.FALLBACK_DATA)
