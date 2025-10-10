# call_trigger.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Config - Using TeleCMI v2 API
APP_ID = os.getenv("APP_ID", "4222424")
APP_SECRET = os.getenv("APP_SECRET", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")
FROM_NUMBER = os.getenv("FROM_NUMBER", "917943446575")  # Your number without +
TO_NUMBER = os.getenv("TO_NUMBER", "917775980069")      # Destination without +

# Correct TeleCMI v2 API endpoint
TELEcMI_API_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"

def make_call():
    # Payload structure WITHOUT answer_url
    payload = {
        "appid": int(APP_ID),
        "secret": APP_SECRET,
        "from": FROM_NUMBER,
        "to": TO_NUMBER,
        "extra_params": {
            "test_id": "IVR_TEST_001"
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
        print("📞 Making call with configuration:")
        print(f"From: {FROM_NUMBER}")
        print(f"To: {TO_NUMBER}")
        print(f"API URL: {TELEcMI_API_URL}")
        
        res = requests.post(TELEcMI_API_URL, json=payload, headers=headers, timeout=15)
        
        print(f"📊 Status Code: {res.status_code}")
        print(f"📄 Response: {res.text}")
        
        res.raise_for_status()
        
        try:
            data = res.json()
            if data.get('status') == 'error':
                print("❌ Call failed with error!")
            else:
                print("✅ Call triggered successfully!")
            print("Response data:", data)
            return data
        except ValueError:
            print("Response (text):", res.text)
            return {"text_response": res.text}
            
    except requests.exceptions.RequestException as e:
        print("❌ Error triggering call:", e)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error response: {e.response.text}")
        return None

if __name__ == "__main__":
    make_call()