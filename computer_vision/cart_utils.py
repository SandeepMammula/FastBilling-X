import time
from collections import defaultdict
import requests

DEBOUNCE_SECONDS = 2.0
cart = defaultdict(int)
last_detected_time = {}

BACKEND_URL = "http://127.0.0.1:8000/cart/add"  

def update_cart(item):
    """Update local cart and send API request to MongoDB backend."""
    current_time = time.time()
    if item not in last_detected_time or current_time - last_detected_time[item] > DEBOUNCE_SECONDS:
        cart[item] += 1
        last_detected_time[item] = current_time
        print(f"[CART] Added: {item} | Total Count: {cart[item]}")
        try:
            requests.post(BACKEND_URL, json={"item_name": item, "quantity": 1})
        except Exception as e:
            print(f"[ERROR] Could not update backend: {e}")
