from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory database simulation
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    fake_items_db.append(item.dict())
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id >= len(fake_items_db) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]
