# call_trigger.py
import requests

def make_call():
    # Your Render app URL - UPDATE THIS AFTER DEPLOYMENT
    ANSWER_URL = "https://call-ivr.onrender.com/call"
    
    payload = {
        "appid": "4222424",  # String for v1 API
        "secret": "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780",
        "from": "917943446575",  # String for v1 API
        "to": "917775980069",    # String for v1 API
        "answer_url": ANSWER_URL  # This is REQUIRED for voice
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Making call with Piopiy v1 API...")
        print(f"From: 917943446575")
        print(f"To: 917775980069")
        print(f"Answer URL: {ANSWER_URL}")
        
        # Use Piopiy v1 API for voice support
        response = requests.post(
            "https://piopiy.telecmi.com/v1/call/make",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Call initiated with voice support!")
            return response.json()
        else:
            print("❌ Call failed")
            return None
            
    except Exception as e:
        print(f"💥 Error: {e}")
        return None

if __name__ == "__main__":
    make_call()