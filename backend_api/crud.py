from backend_api.db import cart_collection

def add_item_to_db(item_name: str, quantity: int):
    existing = cart_collection.find_one({"item_name": item_name})
    if existing:
        cart_collection.update_one(
            {"item_name": item_name},
            {"$inc": {"quantity": quantity}}
        )
    else:
        cart_collection.insert_one({"item_name": item_name, "quantity": quantity})

def get_cart_items():
    return list(cart_collection.find({}, {"_id": 0}))

