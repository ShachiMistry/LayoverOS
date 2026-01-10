import os
import json
import time
from pymongo import MongoClient
from langchain_voyageai import VoyageAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

# Configuration
MONGO_URI = os.getenv("MONGO_URI")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
DB_NAME = "LayoverOS"
COLLECTION_NAME = "amenities"

def seed_data():
    if not MONGO_URI or not VOYAGE_API_KEY:
        print("❌ Error: MONGO_URI or VOYAGE_API_KEY not found in .env")
        return

    print("🔌 Connecting to MongoDB...")
    try:
        client = MongoClient(MONGO_URI)
        collection = client[DB_NAME][COLLECTION_NAME]
        print("✅ Connected!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Load Data
    try:
        with open("sfo_amenities.json", "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("❌ sfo_amenities.json not found! Run get_sfo_data.py first.")
        return

    print(f"📦 Loaded {len(raw_data)} amenities from JSON.")

    # Convert to LangChain Documents
    docs = []
    for item in raw_data:
        # Create a rich description for embedding
        page_content = f"{item['name']} ({item['type']}). Located in {item['terminal']}. {item.get('desc', '')}"
        
        metadata = {
            "name": item["name"],
            "type": item["type"],
            "terminal": item["terminal"],
            "status": "OPEN", # Default status for simulation
            "wait_time": "5 mins",
            "lat": item["lat"],
            "lon": item["lon"]
        }
        docs.append(Document(page_content=page_content, metadata=metadata))

    # Initialize Embedding Model
    print("🧠 Initializing Voyage AI Embeddings...")
    embeddings = VoyageAIEmbeddings(
        model="voyage-3-large", 
        voyage_api_key=VOYAGE_API_KEY
    )

    # Ingest into MongoDB
    print("🚀 Ingesting data into MongoDB Atlas Vector Store...")
    # This automatically generates embeddings and inserts docs
    MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index" 
    )

    print("✅ Success! Database seeded.")
    print("\n⚠️  IMPORTANT: Now go to Atlas UI -> Search -> Create Index (JSON Editor) and paste this:")
    print("-" * 50)
    print("""
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1024,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "status"
    },
    {
      "type": "filter",
      "path": "terminal"
    }
  ]
}
    """)
    print("-" * 50)

if __name__ == "__main__":
    seed_data()
