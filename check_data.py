import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), tlsAllowInvalidCertificates=True)
db = client["layover_os"]
collection = db["amenities"]

sfo_count = collection.count_documents({"airport_code": "SFO"})
print(f"✅ Total SFO Amenities: {sfo_count}")

# Breakdown by terminal
pipeline = [
    {"$match": {"airport_code": "SFO"}},
    {"$group": {"_id": "$terminal_id", "count": {"$sum": 1}}}
]
print("📊 Breakdown by Terminal:")
for doc in collection.aggregate(pipeline):
    print(f"   {doc['_id']}: {doc['count']}")
