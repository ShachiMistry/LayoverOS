import requests
import json
import time

URL = "http://localhost:8000/chat"

test_cases = [
    {
        "name": "☕ Amenity Search (Coffee)",
        "input": "Where is the nearest coffee?",
        "expected_type": "amenity",
        "forbidden_text": "flight number"
    },
    {
        "name": "✈️ Flight Tracking (Explicit)",
        "input": "Status of flight UA400",
        "expected_type": "flight",
        "required_text": "Denver" # UA400 goes to Denver in our seed data
    },
    {
        "name": "📍 Location Context (The 'SFO' Fix)",
        "input": "I am at SFO",
        "expected_type": "amenity", # Should act as general concierge, not flight tracker
        "forbidden_text": "flight number"
    },
    {
        "name": "🚽 Restroom Search",
        "input": "Where are the restrooms?",
        "expected_type": "amenity",
        "forbidden_text": "flight number"
    },
    {
        "name": "🗺️ Navigation",
        "input": "How do I get to Terminal 3?",
        "expected_type": "amenity",
        "forbidden_text": "flight number"
    }
]

def run_tests():
    print("🚦 Starting Dual-Mode Routing Checks...\n")
    
    for test in test_cases:
        print(f"Testing: {test['name']}")
        print(f"   Input: '{test['input']}'")
        
        try:
            payload = {
                "message": test['input'],
                "thread_id": f"test_{int(time.time())}", # New thread each time to reset state
                "user_location": "SFO",
                "airport_code": "SFO"
            }
            
            start = time.time()
            response = requests.post(URL, json=payload).json()
            duration = time.time() - start
            
            output_msg = response.get('response', 'No response text')
            
            # Validation Logic
            passed = True
            reason = ""
            
            if "forbidden_text" in test and test["forbidden_text"].lower() in output_msg.lower():
                passed = False
                reason = f"❌ Failed! Agent wrongly asked for '{test['forbidden_text']}'"
                
            if "required_text" in test and test["required_text"].lower() not in output_msg.lower():
                passed = False
                reason = f"❌ Failed! Response missing '{test['required_text']}'"
                
            if passed:
                print(f"   ✅ PASS ({duration:.2f}s)")
                # print(f"      Response: \"{output_msg[:60]}...\"")
            else:
                print(f"   {reason}")
                print(f"      Response: \"{output_msg}\"")
                
        except Exception as e:
            print(f"   ❌ CRITICAL ERROR: {e}")
            
        print("-" * 40)

if __name__ == "__main__":
    run_tests()
