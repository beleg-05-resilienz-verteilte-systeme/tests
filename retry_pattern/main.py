import os
import logging
import requests

from requests.exceptions import HTTPError
from fastapi import FastAPI, HTTPException
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_fixed,
    before_log,
    after_log,
    RetryError
)

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Externer Service zum Simulieren eines Fehlers
EXTERNAL_SERVICE_URL = os.getenv("EXTERNAL_SERVICE_URL")
STOP_AFTER_ATTEMPT = os.getenv("STOP_AFTER_ATTEMPT", 3)
WAIT_FIXED = os.getenv("WAIT_FIXED", 1)

# Retry-Konfiguration mit Tenacity
@retry(
    stop = stop_after_attempt(STOP_AFTER_ATTEMPT),
    wait = wait_fixed(WAIT_FIXED),
    before = before_log(logger, logging.INFO),
    after = after_log(logger, logging.INFO)
)
def fetch_data():
    logger.info("Sende Anfrage an externen Dienst...")
    response = requests.get(EXTERNAL_SERVICE_URL)
    response.raise_for_status()
    return response.json()

@app.get("/get-data")
def get_data():
    data = fetch_data()
    return {
        "success": True,
        "data": data
    }
