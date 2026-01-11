import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("❌ Error: Missing MONGO_URI")
    exit(1)

client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client["layover_os"] # Match agent_graph.py
flights = db["flights"]

# Data for demo
flight_data = {
    "flight_number": "UA400",
    "airline": "United Airlines",
    "origin": "SFO",
    "destination": "DEN",
    "status": "On Time",
    "gate": "F12",
    "terminal": "3",
    "departure_time": "10:30 AM",
    "arrival_time": "02:00 PM"
}

# Delete existing to avoid dups
flights.delete_many({"flight_number": "UA400"})

# Insert
flights.insert_one(flight_data)

print("✅ Seeded Flight UA400 into 'layover_os.flights'")
print(flight_data)
