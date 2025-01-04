import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from tenacity import RetryError

from retry_pattern import main

class TestRetryPattern(unittest.TestCase):
    
    def setUp(self):
        self.stop_after_attempt = main.STOP_AFTER_ATTEMPT
        self.client = TestClient(main.app)

    @patch("requests.get")
    def test_get_data_success(self, mock_get):
        """Test fetch_data when the external service responds successfully."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { "message": "Success" }

        response = self.client.get("/get-data/")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['data'], {"message": "Success"})
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_data_partial_fail_then_success(self, mock_get):
        """Test fetch_data when it fails initially but succeeds before max retries."""
        # Simulate failure for the first two calls, success on the third

        mock_get_success = MagicMock()
        mock_get_success.status_code = 200
        mock_get_success.json.return_value = { "message": "Success" }

        effects = [
            HTTPException(status_code = 500, detail = "Internal Server Error")
            for _ in range(self.stop_after_attempt - 1)
        ]
        effects.append(mock_get_success)
        mock_get.side_effect = effects

        response = self.client.get("/get-data/")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_get.call_count, self.stop_after_attempt)
        self.assertEqual(response_data['data'], { "message": "Success" })

    @patch("requests.get")
    def test_get_data_retry_and_fail(self, mock_get):
        """Test fetch_data when all retry attempts fail."""
        # Simulate the external service returning 500 errors
        mock_get.side_effect = HTTPException(status_code = 500, detail = "Internal Server Error")

        with self.assertRaises(RetryError):
            self.client.get("/get-data/")

        self.assertEqual(mock_get.call_count, self.stop_after_attempt)
