import os
import pybreaker
import requests
import logging

from fastapi import FastAPI, HTTPException

app = FastAPI()
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

circuit_breaker = pybreaker.CircuitBreaker(
    fail_max = int(os.getenv("MAX_FAILURES", 3)),  # maximale Fehleranzahl
    reset_timeout = int(os.getenv("RESET_TIMEOUT", 10))  # Timeout in Sekunden, bevor der Circuit Breaker zurückgesetzt wird
)

# Externer Service zum Simulieren eines Fehlers
EXTERNAL_SERVICE_URL = os.getenv("EXTERNAL_SERVICE_URL", "http://localhost:80")

@app.get("/get-data")
def get_data():
  try:
    response = circuit_breaker.call(requests.get, EXTERNAL_SERVICE_URL)
    return {
      "success": True,
      "data": response.json()
    }
  
  except pybreaker.CircuitBreakerError as e:
    raise HTTPException(status_code = 503, detail=f"Circuit breaker active: {e}")
  
  except requests.RequestException as e:
    raise HTTPException(status_code = 500, detail=f"Failed to get test data: {e}")
