import os
import operator
import time
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, START, END
from pymongo import MongoClient
from langchain_voyageai import VoyageAIEmbeddings
from langchain_fireworks import ChatFireworks
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
MONGO_URI = os.getenv("MONGO_URI")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
DB_NAME = "layover_os"
COLLECTION_NAME = "amenities"
FLIGHTS_COLLECTION = "flights"
INDEX_NAME = "vector_index"

if not MONGO_URI or not VOYAGE_API_KEY:
    print("❌ ERROR: Missing MONGO_URI or VOYAGE_API_KEY in .env")
    exit(1)

# Initialize Real Connections
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
flights_collection = db[FLIGHTS_COLLECTION]
embeddings = VoyageAIEmbeddings(model="voyage-3-large", voyage_api_key=VOYAGE_API_KEY)

# Initialize LLM (Fireworks)
if FIREWORKS_API_KEY:
    print("🧠 Fireworks AI Connected (Llama-3-70b)")
    llm = ChatFireworks(model="accounts/fireworks/models/llama-v3-70b-instruct", api_key=FIREWORKS_API_KEY)
else:
    print("⚠️ Warning: No FIREWORKS_API_KEY. Agent will use fallback text.")
    llm = None

print("✅ Connected to MongoDB Atlas & Voyage AI")

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    user_location: str   # e.g., "Terminal 2"
    airport_code: str    # e.g., "SFO", "JFK", "DEN"
    next_step: str

# --- NODE DEFINITIONS ---

def supervisor_node(state: AgentState):
    last_message = state['messages'][-1].lower()
    
    # 1. Check for Flight/Trip Intent (Broad detection for "Plan SFO to JFK")
    # We look for "flight", "fly", "trip" OR airport codes pattern
    is_flight_intent = (
        "flight" in last_message or 
        "fly" in last_message or 
        "trip" in last_message or
        " sfo " in last_message or " jfk " in last_message or " den " in last_message
    )
    
    if is_flight_intent:
        return {"next_step": "flight_tracker"}
        
    # 2. Check for Payment Intent
    elif "buy" in last_message or "pay" in last_message:
        return {"next_step": "bursar"}
        
    # 3. Default: Keyword Search (Adaptive: No flight info needed)
    else:
        return {"next_step": "scout"}

def scout_node(state: AgentState):
    query_text = state['messages'][-1]
    airport = state.get('airport_code', 'SFO') # Default to SFO
    
    print(f"\n[Scout] Searching '{query_text}' in {airport}...")
    
    query_vector = embeddings.embed_query(query_text)
    
    # --- PRO FILTERING ---
    # We only show results for the CURRENT AIRPORT
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": INDEX_NAME,
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 10,
                "filter": {
                    "airport_code": {"$eq": airport}
                }
            }
        },
        {"$limit": 3}, # Take top 3 after filter
        {
            "$project": {
                "name": 1, 
                "description_for_embedding": 1, 
                "metadata": 1,
                "terminal_id": 1,
                "airport_code": 1
            }
        }
    ])
    
    found_items = []
    for r in results:
        name = r.get('name', 'Unknown Place')
        desc = r.get('description_for_embedding', 'No description')
        location = r.get('terminal_id', 'General Area')
        
        # Real-time fields
        meta = r.get('metadata', {})
        is_open = meta.get('is_open_now', True)
        wait = meta.get('wait_time_minutes', 0)
        
        status_icon = "🟢 OPEN" if is_open else "🔴 CLOSED"
        
        found_items.append(
            f"- **{name}** ({location})\n"
            f"  Status: {status_icon} | Wait: {wait}m\n"
            f"  {desc}"
        )
    
    if not found_items:
        response = f"Scout: I couldn't find anything matching '{query_text}' at {airport}."
    else:
        context = "\n".join(found_items)
        if llm:
             # Natural Language Synthesis
            sys_msg = SystemMessage(
                content=f"You are LayoverOS, a helpful airport concierge at {airport}. "
                        "Answer the user's request based ONLY on the provided amenities context. "
                        "Keep it short, friendly, and helpful. Mention the location (terminal) and status (open/closed)."
            )
            human_msg = HumanMessage(content=f"User Request: {query_text}\n\nContext Options:\n{context}")
            try:
                ai_msg = llm.invoke([sys_msg, human_msg])
                response = ai_msg.content
            except Exception as e:
                response = f"Scout (Fallback): Here are the options:\n{context}"
        else:
            # Fallback
            response = f"Scout: Here are the top options at {airport}:\n\n" + "\n".join(found_items)
        
    return {"messages": [response]}

def flight_node(state: AgentState):
    """
    Looks up flight details in the 'flights' collection.
    """
    last_message = state['messages'][-1].upper()
    print(f"\n[FlightTracker] Analyzing: {last_message}")
    
    # Simple extraction: look for typical flight codes like "UA123"
    # In a hackathon, we can just search the collection for *any* match in the text
    # or grab the first word that looks like a flight number.
    
    # Strategy: Regex or just simple substring search if logic is too complex
    # Let's try searching text index if it exists, or just regex find
    
    # Hackathon Shortcut: Search for typical prefixes
    import re
    match = re.search(r'([A-Z]{2}\d{3,4})', last_message)
    
    if match:
        flight_num = match.group(1)
        print(f"Detected Flight Number: {flight_num}")
        
        doc = flights_collection.find_one({"flight_number": flight_num})
        
        if doc:
            status = doc.get('status', 'Unknown')
            gate = doc.get('gate', 'TBD')
            dest = doc.get('destination', 'Unknown')
            
            if llm:
                sys_msg = SystemMessage(content="You are a Flight Tracker. Inform the user about their flight status clearly.")
                human_msg = HumanMessage(content=f"Flight: {flight_num} to {dest}. Status: {status}. Gate: {gate}. \nUser asked: {last_message}")
                ai_msg = llm.invoke([sys_msg, human_msg])
                response = ai_msg.content
            else:
                response = f"✈️ **Flight {flight_num} to {dest}**\nStatus: **{status}**\nGate: {gate}"
        else:
            response = f"FlightTracker: I couldn't find flight {flight_num} in our database."
    else:
        # Fallback search in flights collection using text if no regex match?
        # For hackathon, just ask for clarity
        response = "FlightTracker: Please provide a valid flight number (e.g., UA450)."
        
    return {"messages": [response]}

def bursar_node(state: AgentState):
    print("\n[Bursar] Processing Payment...")
    return {"messages": ["Bursar: Payment of $50 USDC successful. Access Granted."]}

# --- GRAPH CONSTRUCTION ---

builder = StateGraph(AgentState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("scout", scout_node)
builder.add_node("flight_tracker", flight_node)
builder.add_node("bursar", bursar_node)

builder.add_edge(START, "supervisor")

def router(state: AgentState):
    return state["next_step"]

builder.add_conditional_edges(
    "supervisor",
    router,
    {
        "scout": "scout",
        "flight_tracker": "flight_tracker",
        "bursar": "bursar"
    }
)

builder.add_edge("scout", END)
builder.add_edge("flight_tracker", END)
builder.add_edge("bursar", END)

# --- PERSISTENCE (THE "OFFLINE" BRAIN) ---
from langgraph.checkpoint.mongodb import MongoDBSaver

# Initialize Checkpointer
# This saves every "thought" to MongoDB so if WiFi dies, we remember everything.
checkpointer = MongoDBSaver(client)

app = builder.compile(checkpointer=checkpointer)

# --- CLI TEST RUNNER ---
if __name__ == "__main__":
    print("🚀 LayoverOS (REAL MODE) Started.")
    
    # Mock Config
    config = {"configurable": {"thread_id": "test_thread"}}
    current_state = {
        "messages": [], 
        "user_location": "Terminal 2",
        "airport_code": "SFO" # Default for CLI
    }
    
    while True:
        try:
            user_input = input("\nUser (Type 'quit' to exit): ")
            if user_input.lower() in ["quit", "exit"]:
                break
            
            # Allow CLI user to switch airport context manually for testing
            if user_input.startswith("/airport"):
                new_code = user_input.split(" ")[1].upper()
                current_state["airport_code"] = new_code
                print(f"✈️ Switched context to {new_code}")
                continue

            current_state["messages"].append(user_input)
            output = app.invoke(current_state, config=config)
            print(f"\n{output['messages'][-1]}")
            current_state = output
        except Exception as e:
            print(f"Error: {e}")
