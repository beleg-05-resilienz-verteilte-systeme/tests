from fastapi import FastAPI, HTTPException
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
    return {"message": "Willkommen bei der FastAPI-Testanwendung"}

# GET-Endpoint
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "query": q}

# POST-Endpoint
@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

# PUT-Endpoint
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item}