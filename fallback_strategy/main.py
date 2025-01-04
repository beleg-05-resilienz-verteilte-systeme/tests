from fastapi import FastAPI
from fastapi.responses import JSONResponse

import logging
import requests

from requests.exceptions import HTTPError

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()

EXTERNAL_SERVICE_URL = "http://localhost:8000/test-data"

FALLBACK_DATA = [
    {"title": "Lorem Ipsum: The Beginning", "author": "John Doe", "year": 2020},
    {"title": "Dolor Sit Amet", "author": "Jane Smith", "year": 2019},
    {"title": "Consectetur Adipiscing Elit", "author": "Alice Johnson", "year": 2021},
    {"title": "Sed Do Eiusmod", "author": "Bob Brown", "year": 2018},
    {"title": "Tempor Incididunt", "author": "Charlie Davis", "year": 2022}
]

@app.get("/get-data/")
def get_data():
  try:
    response = requests.get(EXTERNAL_SERVICE_URL)
    response.raise_for_status()

    print(response.status_code)

    return JSONResponse(
        content = {
            "success": True,
            "data": response.json()
        }
    )
  
  except (requests.RequestException, requests.exceptions.HTTPError) as e:
    logger.error(f"Failed to fetch data from {EXTERNAL_SERVICE_URL}: {e}")
    return JSONResponse(
        content = {
            "success": False,
            "data": FALLBACK_DATA
        }
    )
