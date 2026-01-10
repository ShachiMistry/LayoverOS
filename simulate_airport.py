import time
import random
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "layover_os"     # Updated to match screenshot (lowercase)
COLLECTION_NAME = "amenities"

def simulate_airport_events():
    if not MONGO_URI:
        print("⚠️  MONGO_URI not found. Please set it in .env")
        exit(1)

    print("🔌 Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
    collection = client[DB_NAME][COLLECTION_NAME]
    
    # Check if connected
    try:
        count = collection.count_documents({})
        print(f"✅ Connected. Found {count} amenities to simulate.")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        exit(1)

    print("\n✈️  LAYOVER OS: SFO DIGITAL TWIN STARTED")
    print("   Broadcasting real-time status updates...")
    print("-" * 60)
    
    # We update these fields based on the screenshot schema:
    # metadata.is_open_now (boolean)
    # metadata.wait_time_minutes (int)
    
    amenities = list(collection.find({}, {"_id": 1, "name": 1}))
    
    if not amenities:
        print("❌ No amenities found!")
        exit(1)

    while True:
        # Pick a random place
        target = random.choice(amenities)
        name = target.get("name", "Unknown")
        
        # New randomized state
        is_open = random.choice([True, True, True, False]) # Mostly open
        wait_time = random.randint(5, 60) if is_open else 0
        
        # Update MongoDB
        collection.update_one(
            {"_id": target["_id"]},
            {"$set": {
                "metadata.is_open_now": is_open,
                "metadata.wait_time_minutes": wait_time,
                "metadata.last_updated_ts": time.time()
            }}
        )
        
        status_str = "OPEN" if is_open else "CLOSED"
        timestamp = time.strftime("%H:%M:%S")
        
        print(f"[{timestamp}] 🔄 {name:<30} | {status_str:<6} | Wait: {wait_time}m")
        
        time.sleep(random.randint(2, 4)) # Fast updates for demo

if __name__ == "__main__":
    simulate_airport_events()
