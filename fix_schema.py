import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client["layover_os"]
collection = db["amenities"]

print("🔄 Starting Migration: terminal -> terminal_id")

# Update all documents that have 'terminal' but missing 'terminal_id'
# using an aggregation pipeline for efficiency
result = collection.update_many(
    {"terminal": {"$exists": True}},
    [{"$set": {"terminal_id": "$terminal"}}]
)

print(f"✅ Matched {result.matched_count} documents.")
print(f"✅ Modified {result.modified_count} documents.")

# Verify
doc = collection.find_one()
print("\n🔍 Sample Document After Fix:")
print(f"Name: {doc.get('name')}")
print(f"Terminal: {doc.get('terminal')}")
print(f"Terminal ID: {doc.get('terminal_id')}")
