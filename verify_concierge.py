import requests
import json

url = "http://localhost:8000/chat"
payload = {
    "message": "I am at SFO",
    "user_location": "Unknown",
    "airport_code": "SFO"
}

print("🗣️ Sending: 'I am at SFO'")
print("🗣️ Sending: 'I am at SFO'")
try:
    res = requests.post(url, json=payload)
    print(f"Status Code: {res.status_code}")
    print(f"Full JSON: {res.json()}")
    
    if res.status_code == 200:
        response_text = res.json().get('response', 'No response key')
        print(f"🤖 Agent Response:\n{response_text}")
except Exception as e:
    print(f"❌ Error: {e}")
