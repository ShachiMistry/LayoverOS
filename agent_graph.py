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
    print("🧠 Fireworks AI Connected (Mixtral-8x7b)")
    llm = ChatFireworks(
        # model="accounts/fireworks/models/llama-v3p3-70b-instruct", 
        model="accounts/fireworks/models/mixtral-8x7b-instruct",
        api_key=FIREWORKS_API_KEY,
        max_retries=0,
        request_timeout=5
    )
else:
    print("⚠️ Warning: No FIREWORKS_API_KEY. Agent will use fallback text.")
    llm = None

print("✅ Connected to MongoDB Atlas & Voyage AI")

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    user_location: str   # e.g., "Terminal 2"
    airport_code: str    # e.g., "SFO", "JFK", "DEN"
    flight_number: str   # e.g., "UA400" (Persisted)
    next_step: str

# --- NODE DEFINITIONS ---

def supervisor_node(state: AgentState):
    raw_msg = state['messages'][-1]
    if hasattr(raw_msg, 'content'):
        last_message = raw_msg.content.lower()
    else:
        last_message = str(raw_msg).lower()
    
    import re
    
    # 0. Context Switching (Airport Code)
    # Check if user mentioned a supported airport to switch context
    found_airport = None
    for code in ["SFO", "JFK", "DEN"]:
        if code in last_message.upper():
            found_airport = code
            print(f"✈️ Context Switch Detected: {found_airport}")
            break
            
    # 1. Check for Strong Flight Signals
    # We only trigger flight logic if user EXPLICITLY asks for it or provides a code (e.g. UA400)
    has_flight_code = re.search(r'[A-Z]{2}\d{3,4}', last_message.upper())
    has_flight_keyword = any(kw in last_message for kw in ["flight", "fly", "airline", "boarding"])
    is_planning_trip = "plan" in last_message and "to" in last_message # e.g. "Plan trip to JFK"
    
    if has_flight_keyword or has_flight_code or is_planning_trip:
        return {"next_step": "flight_tracker", "airport_code": found_airport} if found_airport else {"next_step": "flight_tracker"}
        
    # 2. Check for Payment Intent
    elif any(kw in last_message for kw in ["buy", "pay", "book", "purchase", "reserve"]):
        return {"next_step": "bursar", "airport_code": found_airport} if found_airport else {"next_step": "bursar"}
        
    # 3. Default: Amenity Search (The Safety Net)
    # "I am at SFO" -> Scout
    # "Where is coffee?" -> Scout
    else:
        return {"next_step": "scout", "airport_code": found_airport} if found_airport else {"next_step": "scout"}

def scout_node(state: AgentState):
    raw_msg = state['messages'][-1]
    if hasattr(raw_msg, 'content'):
        query_text = raw_msg.content
    else:
        query_text = str(raw_msg)
    airport = state.get('airport_code', 'SFO') # Default to SFO
    
    print(f"\n[Scout] Searching '{query_text}' in {airport}...")

    # --- CONCIERGE MODE (Context Setting) ---
    # If user just says "I am at SFO", don't search. Ask for details.
    if len(query_text.split()) < 5 and ("at" in query_text.lower() or "in" in query_text.lower()) and airport.lower() in query_text.lower():
        # User is setting context: "I am at SFO"
        if llm:
            try:
                sys_msg = SystemMessage(content=f"You are a helpful Concierge at {airport}. The user just arrived. Ask them TWO things: which Terminal they are in, and what amenity they are looking for. Keep it short.")
                human_msg = HumanMessage(content=query_text)
                ai_msg = llm.invoke([sys_msg, human_msg])
                return {"messages": [ai_msg.content]}
            except Exception as e:
                print(f"❌ LLM Concierge Error: {e}")
                return {"messages": ["Concierge: Which terminal are you in, and what do you need?"]}
        else:
            return {"messages": ["Concierge: Which terminal are you in, and what do you need?"]}
    
    query_vector = embeddings.embed_query(query_text)
    
    # --- TERMINAL FILTERING ---
    import re
    terminal_match = re.search(r'Terminal\s+(\w+)', query_text, re.IGNORECASE)
    
    # Base filter: Airport matches
    search_filter = {"airport_code": {"$eq": airport}}
    
    if terminal_match:
        target_terminal = terminal_match.group(1)
        # Try to match the format in DB (usually just the number/letter)
        # We add it to the filter logic
        print(f"🎯 Filtering for Terminal: {target_terminal}")
        search_filter["terminal_id"] = {"$eq": target_terminal}

    # --- PRO FILTERING ---
    # We only show results for the CURRENT AIRPORT (and Terminal if specified)
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": INDEX_NAME,
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 10,
                "filter": search_filter
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
                content=f"You are LayoverOS, an advanced operating system for travel. {airport}. "
                        "The user is on a layover. Optimize their time based on the amenities found. "
                        "Keep it short, professional, and helpful. Mention the location (terminal) and status."
            )
            human_msg = HumanMessage(content=f"User Request: {query_text}\n\nContext Options:\n{context}")
            try:
                ai_msg = llm.invoke([sys_msg, human_msg])
                response = ai_msg.content
            except Exception as e:
                print(f"❌ LLM Error: {e}") 
                # Hackathon Fix: Hide the ugly error from the UI. User just wants results.
                response = f"Scout: Here are the top options I found for you:\n{context}"
        else:
            # Fallback
            response = f"Scout: Here are the top options at {airport}:\n\n" + "\n".join(found_items)
        
    return {"messages": [response]}

def flight_node(state: AgentState):
    """
    Looks up flight details in the 'flights' collection.
    """
    raw_msg = state['messages'][-1]
    if hasattr(raw_msg, 'content'):
        last_message = raw_msg.content.upper()
    else:
        last_message = str(raw_msg).upper()
    print(f"\n[FlightTracker] Analyzing: {last_message}")
    
    # Simple extraction: look for typical flight codes like "UA123"
    # In a hackathon, we can just search the collection for *any* match in the text
    # or grab the first word that looks like a flight number.
    
    # Strategy: Regex or just simple substring search if logic is too complex
    # Let's try searching text index if it exists, or just regex find
    
    # Hackathon Shortcut: Search for typical prefixes
    import re
    # 1. Try to find in current message
    import re
    match = re.search(r'([A-Z]{2}\d{3,4})', last_message)
    
    current_flight = state.get('flight_number')
    
    if match:
        flight_num = match.group(1)
        print(f"Detected Flight Number: {flight_num}")
        # SAVE TO STATE!
        # (Note: In LangGraph, returning a key updates that key in the state)
        
    elif current_flight:
        # Use memory
        flight_num = current_flight
        print(f"Using Remembered Flight: {flight_num}")
    else:
        flight_num = None

    if flight_num:
        doc = flights_collection.find_one({"flight_number": flight_num})
        
        if doc:
            status = doc.get('status', 'Unknown')
            gate = doc.get('gate', 'TBD')
            dest = doc.get('destination', 'Unknown')
            
            if llm:
                try:
                    sys_msg = SystemMessage(content="You are a Flight Tracker. Inform the user about their flight status clearly.")
                    # We mention the flight number in the human msg context so LLM knows it
                    human_msg = HumanMessage(content=f"Flight: {flight_num} to {dest}. Status: {status}. Gate: {gate}. \nUser asked: {last_message}")
                    ai_msg = llm.invoke([sys_msg, human_msg])
                    response = ai_msg.content
                except Exception as e:
                    print(f"❌ LLM Error (FlightNode): {e}")
                    response = f"✈️ **Flight {flight_num} to {dest}**\nStatus: **{status}**\nGate: {gate}"
            else:
                response = f"✈️ **Flight {flight_num} to {dest}**\nStatus: **{status}**\nGate: {gate}"
                
            return {"messages": [response], "flight_number": flight_num}
        else:
            # If not found, CLEAR the state so we don't get stuck on a typo
            response = f"FlightTracker: I couldn't find flight {flight_num} in our database. Please double-check the number (e.g., UA400)."
            return {"messages": [response], "flight_number": ""}
    else:
        # Fallback search in flights collection using text if no regex match?
        # For hackathon, just ask for clarity
        if llm:
            try:
                 response = llm.invoke("User wants to find a flight but didn't provide a number. Ask them for it politely. Keep it short.").content
            except Exception as e:
                 print(f"❌ LLM Flight Fallback Error: {e}")
                 response = "FlightTracker: I can help with that. What is the flight number? (e.g., UA400)"
        else:
             response = "FlightTracker: I can help with that. What is the flight number? (e.g., UA400)"
             
        return {"messages": [response]}

def bursar_node(state: AgentState):
    print("\n[Bursar] Processing Payment...")
    # We send a special tag that the Frontend recognizes to open the Modal
    return {"messages": ["Bursar: I have located the United Club in Terminal 3. Access is $50. Opening secure payment gateway... [PAYMENT_REQUIRED]"]}

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
