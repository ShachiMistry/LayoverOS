import requests

url = "http://localhost:8000/chat"

# Case: User tries to switch to JFK
payload = {
    "message": "I am at JFK", 
    "user_location": "Unknown",
    # Note: frontend sends default 'SFO', but the MESSAGE should override it in a smart agent.
    # However, let's see what happens if we rely on the message.
    "airport_code": "SFO" 
}

print("🗣️ Sending: 'I am at JFK' (while current state is SFO)")
try:
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        data = res.json()
        print(f"🤖 Response: {data['response']}")
        
        # Check if response mentions JFK
        if "Welcome to JFK" in data['response'] or "concierge at JFK" in data['response']:
             print("✅ PASS: Context switched to JFK.")
        else:
             print("❌ FAIL: Context remained at SFO (or generic).")
    else:
        print(f"❌ Error: {res.status_code}")
except Exception as e:
    print(f"❌ Exception: {e}")
