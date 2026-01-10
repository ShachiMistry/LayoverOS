import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("❌ Error: Missing MONGO_URI")
    exit(1)

client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client["layover_os"]

def print_doc(name, collection):
    print(f"\n🔍 Inspecting Collection: '{name}'")
    try:
        count = collection.count_documents({})
        print(f"   Count: {count} documents")
        doc = collection.find_one()
        if doc:
            print(f"   Sample Document:\n{doc}")
        else:
            print("   ⚠️  Collection is empty.")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print_doc("flights", db["flights"])
print_doc("amenities", db["amenities"])
