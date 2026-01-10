import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_voyageai import VoyageAIEmbeddings

# Load env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
DB_NAME = "layover_os"
COLLECTION_NAME = "amenities"
INDEX_NAME = "vector_index"

def verify_search():
    print("🔍 [Verification] Connecting to MongoDB Atlas & Voyage AI...")
    
    if not MONGO_URI or not VOYAGE_API_KEY:
        print("❌ Error: Missing credentials in .env")
        return

    try:
        # 1. Connect
        client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # 2. Embed Query
        embeddings = VoyageAIEmbeddings(model="voyage-3-large", voyage_api_key=VOYAGE_API_KEY)
        query = "Where can I get some coffee?"
        print(f"✨ Embedding Query: '{query}'")
        query_vector = embeddings.embed_query(query)
        
        # 3. Vector Search
        print("🚀 Executing $vectorSearch on Atlas...")
        start_time = time.time()
        
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": INDEX_NAME,
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": 100,
                    "limit": 5
                }
            },
            {
                "$project": {
                    "name": 1, 
                    "description_for_embedding": 1, 
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ])
        
        elapsed = time.time() - start_time
        print(f"✅ Search Complete in {elapsed:.2f} seconds.")
        
        # 4. Print Results
        items = list(results)
        if items:
            print(f"\n🎯 Found {len(items)} Matches:")
            for i, item in enumerate(items):
                print(f"   {i+1}. {item.get('name')} (Score: {item.get('score', 'N/A')})")
                print(f"      Desc: {item.get('description_for_embedding')[:100]}...")
        else:
            print("\n⚠️ No results found. Check if the database 'amenities' collection has data and the Vector Index is active.")

    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")

if __name__ == "__main__":
    verify_search()
