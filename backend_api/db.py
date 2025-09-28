from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") 
db = client["fastbillingx"]                        
cart_collection = db["cart_items"]                 
