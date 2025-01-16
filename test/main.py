from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Beispiel-Datenmodell
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool = False

# Root-Endpunkt
@app.get("/")
async def read_root():
    return { "message": "Willkommen bei der FastAPI-Testanwendung" }

@app.get("/data")
async def read_root():
    return { "data": "Hello world !" }
