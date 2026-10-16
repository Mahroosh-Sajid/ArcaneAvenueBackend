from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["arcane_avenue"]
users=db["users"]
#filters
users.create_index("email", unique=True)

test_collection= db["test_collection"]
users.create_index("email", unique=True)