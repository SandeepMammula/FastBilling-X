from fastapi import FastAPI
from pydantic import BaseModel
from backend_api import crud

app = FastAPI()

class CartItem(BaseModel):
    item_name: str
    quantity: int

@app.post("/cart/add")
def add_item(item: CartItem):
    """Add an item to MongoDB cart."""
    crud.add_item_to_db(item.item_name, item.quantity)
    return {"status": "success", "item": item.item_name, "quantity": item.quantity}

@app.get("/cart")
def get_cart():
    """Get current cart items."""
    return crud.get_cart_items()


