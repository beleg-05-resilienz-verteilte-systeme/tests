import time, unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from circuit_breaker import main

class TestCircuitBreaker(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(main.app)
        self.circuit_breaker = main.circuit_breaker
        self.circuit_breaker.close()

    @patch("requests.get")
    def test_get_data_success(self, mock_get: MagicMock):
        
        mock_response = { "message": "test" }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        response = self.client.get("/get-data")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertEqual(response_data["data"], mock_response)

    @patch("requests.get")
    def test_circuit_breaker_failure(self, mock_get: MagicMock):
        
        mock_get.side_effect = HTTPException(status_code = 500)

        # Simulate multiple failures to trip the circuit breaker
        for _ in range(self.circuit_breaker.fail_max):
            self.client.get("/get-data")
        
        # with self.assertRaises(HTTPExceptio) as context:
        response = self.client.get("/get-data")

        self.assertEqual(response.status_code, 503)

    @patch("requests.get")
    def test_reset_circuit_breaker(self, mock_get: MagicMock):
        
        mock_get.side_effect = HTTPException(status_code = 500)

        # Simulate multiple failures
        for _ in range(self.circuit_breaker.fail_max):
            self.client.get("/get-data")

        # Wait for the reset timeout
        time.sleep(self.circuit_breaker.reset_timeout)

        # Test if the circuit breaker is reset
        mock_response = { "message": "test" }   
        mock_get.side_effect = None
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get("/get-data")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertEqual(response_data["data"], mock_response)
