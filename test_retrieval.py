import os
from pymongo import MongoClient
from langchain_voyageai import VoyageAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

if not MONGO_URI or not VOYAGE_API_KEY:
    print("❌ Error: Missing keys in .env")
    exit(1)

client = MongoClient(MONGO_URI)
# Based on screenshots, DB is 'layover_os', Collection is 'amenities'
collection = client["layover_os"]["amenities"]

print("🔍 Connected to MongoDB. Inspecting one document...")
doc = collection.find_one()
print("-" * 30)
print(doc)
print("-" * 30)

print("\n🧪 Testing Vector Search for 'vegan food'...")
try:
    embeddings = VoyageAIEmbeddings(
        model="voyage-3-large", 
        voyage_api_key=VOYAGE_API_KEY
    )
    query = "vegan food"
    query_vec = embeddings.embed_query(query)
    
    # Using the Index Name 'vector_index' from screenshot
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vec,
                "numCandidates": 50,
                "limit": 3
            }
        },
        {"$project": {"name": 1, "description_for_embedding": 1, "metadata": 1, "_id": 0}}
    ])
    
    for r in results:
        print(f"✅ Found: {r.get('name', 'Unknown')}")
        print(f"   Desc: {r.get('description_for_embedding', 'No desc')}")
        print(f"   Metadata: {r.get('metadata', {})}")
        
except Exception as e:
    print(f"❌ Search failed: {e}")
