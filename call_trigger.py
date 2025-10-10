# call_trigger.py - KEEP THIS AS IS
import requests

def make_call():
    payload = {
        "appid": 4222424,
        "secret": "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780",
        "from": 917943446575,
        "to": 917775980069,
        "pcmo": [
            {
                "action": "bridge",
                "duration": 120,
                "timeout": 30,
                "from": 917943446575,
                "connect": [{"type": "pstn", "number": 917775980069}]
            }
        ]
    }
    
    try:
        print("🚀 Triggering call...")
        response = requests.post(
            "https://rest.telecmi.com/v2/ind_pcmo_make_call",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Call initiated!")
        else:
            print("❌ Call failed")
            
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    make_call()