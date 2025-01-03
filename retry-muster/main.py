import os
import logging
import requests

from fastapi import FastAPI, HTTPException
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_fixed,
    before_log,
    after_log
)

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Externer Service zum Simulieren eines Fehlers
EXTERNAL_SERVICE_URL = os.getenv("EXTERNAL_SERVICE_URL")

# Retry-Konfiguration mit Tenacity
@retry(
    stop = stop_after_attempt(3),
    wait = wait_fixed(2),
    before = before_log(logger, logging.INFO),
    after = after_log(logger, logging.INFO)
)
def fetch_data():
    logger.info("Sende Anfrage an externen Dienst...")
    response = requests.get(EXTERNAL_SERVICE_URL)
    response.raise_for_status()  # Löst eine Ausnahme aus, wenn der Statuscode kein 2xx ist
    return response.json()

@app.get("/retry")
def retry_call():
    try:
        data = fetch_data()
        return {
            "status_code": 200,
            "success": True,
            "pattern": "retry-muster",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed after retries: {str(e)}")
