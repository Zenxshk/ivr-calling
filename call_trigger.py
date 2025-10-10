# call_trigger.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Config
APP_ID = os.getenv("APP_ID", "4222424")
APP_SECRET = os.getenv("APP_SECRET", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")
PROVIDER_API = os.getenv("PROVIDER_API", "https://testing.com/v1/call")
FROM_NUMBER = os.getenv("FROM_NUMBER", "+917943446575")
TO_NUMBER = os.getenv("TO_NUMBER", "+917775980069")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

def make_call():
    payload = {
        "from": FROM_NUMBER,
        "to": TO_NUMBER,
        "answer_url": f"{BASE_URL}/call"
    }
    headers = {
        "Content-Type": "application/json",
        "X-App-ID": APP_ID,
        "X-App-Secret": APP_SECRET
    }
    try:
        res = requests.post(PROVIDER_API, json=payload, headers=headers, timeout=15)
        res.raise_for_status()
        try:
            data = res.json()
        except ValueError:
            data = {"text_response": res.text}
        print("Call triggered successfully:", data)
    except requests.exceptions.RequestException as e:
        print("Error triggering call:", e)

if __name__ == "__main__":
    make_call()
