from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["arcane_avenue"]

# getting specific collections we have
users=db["users"]

#optional: if u can't have duplicate value
users.create_index("email", unique=True)