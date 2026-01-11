import os
from agent_graph import app
from dotenv import load_dotenv

load_dotenv()

print("🎬 Running FINAL DEMO VERIFICATION...")

from langchain_core.messages import HumanMessage

def run_query(query, expected_keyword):
    print(f"\n👤 User: {query}")
    result = app.invoke(
        {"messages": [HumanMessage(content=query)], "airport_code": "SFO"},
        {"recursion_limit": 5, "configurable": {"thread_id": "demo_verification_1"}}
    )
    last_msg = result["messages"][-1]
    content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
    
    if expected_keyword in content or expected_keyword in str(result):
        # Check for payment tag specially
        if expected_keyword == "PAYMENT" and "PAYMENT_REQUIRED" in content:
             print(f"✅ SUCCESS: Found trigger '{expected_keyword}'")
             return True
        elif expected_keyword in content:
             print(f"✅ SUCCESS: Response contains '{expected_keyword}'")
             return True
    
    # Check flight node special case
    if "Flight" in str(result) and expected_keyword in str(result):
         print(f"✅ SUCCESS: Flight data found.'")
         return True

    print(f"❌ FAIL: Expected '{expected_keyword}' but got: {content[:100]}...")
    return False

# 1. Context
run_query("I am at SFO", "Welcome") or run_query("I am at SFO", "Concierge")

# 2. Filter Logic (The tricky one)
# We expect "Peet's" or similar from the seeded data for Terminal 2
run_query("Find coffee in Terminal 2", "Terminal 2") 

# 3. Flight
run_query("Track flight UA400", "UA400")

# 4. Payment
run_query("Book a pass for the United Club", "PAYMENT_REQUIRED")
