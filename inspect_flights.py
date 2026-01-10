import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ Error: Missing MONGO_URI in .env")
    exit(1)

client = MongoClient(MONGO_URI)
db = client["layover_os"]
flights_col = db["flights"]

print("🔍 Inspecting 'flights' collection...")
try:
    doc = flights_col.find_one()
    if doc:
        print("✅ Found Flight Document:")
        print(doc)
    else:
        print("⚠️  Collection 'flights' is empty! Ask Shachi to run the seed script.")
except Exception as e:
    print(f"❌ Error: {e}")
