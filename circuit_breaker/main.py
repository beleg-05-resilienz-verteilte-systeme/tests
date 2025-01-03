import os
import pybreaker
import requests
import logging

from fastapi import FastAPI

app = FastAPI()
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

circuit_breaker = pybreaker.CircuitBreaker(
    fail_max = int(os.getenv("MAX_FAILURES")),  # maximale Fehleranzahl
    reset_timeout = int(os.getenv("RESET_TIMEOUT"))  # Timeout in Sekunden, bevor der Circuit Breaker zurückgesetzt wird
)

# Externer Service zum Simulieren eines Fehlers
EXTERNAL_SERVICE_URL = os.getenv("EXTERNAL_SERVICE_URL")

@app.get("/get-data")
def implement_circuit_breaker():
  try:
    response = circuit_breaker.call(requests.get, EXTERNAL_SERVICE_URL)
    return {
      "status_code": 200,
      "success": True,
      "pattern": "circuit_breaker",
      "data": response.json()
    }
  except pybreaker.CircuitBreakerError as e:
    return {
      "status_code": 503,
      "success": False,
      "message": f"Circuit breaker active: {e}"
    }
  except requests.RequestException as e:
    return {
      "status_code": 500,
      "success": False,
      "message": f"Failed get test data: {e}"
    }
  
@app.get("/")
def health_check():
    return {"status": "ok"}

# Endpunkt, um den Status des Circuit Breakers zu überprüfen
@app.get("/status")
def circuit_status():
    return {
       "fail_max": circuit_breaker.fail_max,
       "reset_timeout": circuit_breaker.reset_timeout,
       "circuit_status": circuit_breaker.current_state,
       "fail_counter": circuit_breaker.fail_counter,
    }
