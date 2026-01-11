import requests
import time
import json

URL = "http://localhost:8000/chat"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"

TEST_CASES = [
    # 1. Basic Greeting / Context Setting
    {"msg": "I am at SFO", "desc": "Context Setting (SFO)"},
    
    # 2. Amenity Search (SFO)
    {"msg": "Where can I get coffee?", "desc": "Amenity Search (SFO)"},
    
    # 3. Context Switch to JFK
    {"msg": "I am now at JFK", "desc": "Context Switch -> JFK"},
    
    # 4. Amenity Search (JFK)
    {"msg": "Looking for food here", "desc": "Amenity Search (JFK)"},
    
    # 5. Flight Tracking (Valid)
    {"msg": "What is the status of UA400?", "desc": "Flight Track (Valid)"},
    
    # 6. Flight Tracking (Invalid / Typo)
    {"msg": "Track flight UA99999", "desc": "Flight Track (Invalid)"},
    
    # 7. Payment Trigger
    {"msg": "I want to buy lounge access", "desc": "Payment Intent"},
    
    # 8. Edge Case: Empty/Nonsense
    {"msg": "Blah blah blah", "desc": "Nonsense Input"},
]

def run_tests():
    print(f"{CYAN}🚀 Starting Backend Stress Test...{RESET}\n")
    
    # Keep track of state (like cookie/session) - simplified, we assume stateless API call but backend has DB memory
    # Actually, for the backend to remember "JFK", it relies on the thread_id config in graph.
    # Our simple API endpoint wraps this.
    
    for i, test in enumerate(TEST_CASES):
        print(f"Test {i+1}: {test['desc']}")
        print(f"🗣️  Input: {test['msg']}")
        
        start_time = time.time()
        try:
            payload = {
                "message": test['msg'],
                "user_location": "Test Runner",
                "airport_code": "SFO" # Frontend sends this default, but backend should override if message says JFK
            }
            res = requests.post(URL, json=payload, timeout=10)
            duration = time.time() - start_time
            
            if res.status_code == 200:
                data = res.json()
                response_text = data.get("response", "No response text")
                print(f"🤖 Output: {GREEN}{response_text[:100]}...{RESET}") # Truncate for readability
                print(f"⏱️  Time: {duration:.2f}s")
            else:
                print(f"{RED}❌ Failed: Status {res.status_code}{RESET}")
                
        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}")
            
        print("-" * 40)
        time.sleep(1) # Slight pause between requests

if __name__ == "__main__":
    run_tests()
