# call_trigger.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Config - Using correct Piopiy API endpoint
APP_ID = os.getenv("APP_ID", "4222424")
APP_SECRET = os.getenv("APP_SECRET", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")
PIOPIY_API_URL = "https://piopiy.telecmi.com/v1/call/make"  # Correct endpoint
FROM_NUMBER = os.getenv("FROM_NUMBER", "+917943446575")
TO_NUMBER = os.getenv("TO_NUMBER", "+917775980069")
ANSWER_URL = os.getenv("ANSWER_URL", "https://example.com/call")  # Use your actual answer URL

def make_call():
    payload = {
        "appid": APP_ID,
        "secret": APP_SECRET,
        "from": FROM_NUMBER,
        "to": TO_NUMBER,
        "answer_url": ANSWER_URL
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Making call from {FROM_NUMBER} to {TO_NUMBER}")
        print(f"Using API: {PIOPIY_API_URL}")
        
        res = requests.post(PIOPIY_API_URL, json=payload, headers=headers, timeout=15)
        
        print(f"Response Status: {res.status_code}")
        print(f"Response Text: {res.text}")
        
        res.raise_for_status()
        
        try:
            data = res.json()
            print("Call triggered successfully:", data)
            return data
        except ValueError:
            print("Response (text):", res.text)
            return {"text_response": res.text}
            
    except requests.exceptions.RequestException as e:
        print("Error triggering call:", e)
        return None

if __name__ == "__main__":
    make_call()