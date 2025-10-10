# call_trigger.py
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Your exact credentials from Piopiy dashboard
APP_ID = 4222424  # Must be integer
APP_SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"
FROM_NUMBER = 917943446575  # Must be integer (no quotes)
TO_NUMBER = 917775980069    # Must be integer (no quotes)

# Correct API endpoint from documentation
API_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"

def make_call():
    # Exact payload structure as per TeleCMI documentation
    payload = {
        "appid": APP_ID,
        "secret": APP_SECRET,
        "from": FROM_NUMBER,
        "to": TO_NUMBER,
        "extra_params": {
            "order_id": "TEST123"
        },
        "pcmo": [
            {
                "action": "bridge",
                "duration": 180,
                "timeout": 30,
                "from": FROM_NUMBER,
                "loop": 2,
                "connect": [
                    {
                        "type": "pstn",
                        "number": TO_NUMBER
                    }
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Making call with TeleCMI v2 API...")
        print(f"From: {FROM_NUMBER}")
        print(f"To: {TO_NUMBER}")
        print(f"API: {API_URL}")
        
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'progress':
                print("✅ SUCCESS! Call is ringing!")
                print(f"Request ID: {data.get('request_id')}")
                return data
            else:
                print("❌ API returned error status")
                return data
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"💥 Request failed: {e}")
        return None

if __name__ == "__main__":
    result = make_call()
    if result and result.get('status') == 'progress':
        print("🎉 Call initiated successfully! Phone should ring soon.")
    else:
        print("😞 Call failed. Check the error above.")