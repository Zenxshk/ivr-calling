from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELECMI_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"
APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"

AUDIO_FILE = "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav"


@app.route('/make_call', methods=['GET'])
def make_call():
    """Make outbound call: play audio only (no DTMF input)"""
    payload = {
        "appid": APP_ID,
        "secret": SECRET,
        "from": 917943446575,
        "to": 917756043094,
        "extra_params": {"order_id": "ORD12345"},
        "pcmo": [
            {
                "action": "play",
                "file_name": AUDIO_FILE
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    
    try:
        res = requests.post(TELECMI_URL, json=payload, headers=headers)
        print(f"📞 Call initiated. Status: {res.status_code}")
        print(f"Response: {res.text}")
        return jsonify(res.json())
    except Exception as e:
        print(f"❌ Error making call: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "🎯 IVR Calling System is Running! Use /make_call to start a call."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)