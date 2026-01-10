import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FIREWORKS_API_KEY")

url = "https://api.fireworks.ai/inference/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

print(f"🔍 Querying Fireworks API with Key ending in ...{api_key[-4:] if api_key else 'NONE'}")

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Available Models:")
        for model in data.get('data', []):
            mid = model['id']
            if "llama" in mid.lower() and "instruct" in mid.lower():
                print(f"   - {mid}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Exception: {e}")
