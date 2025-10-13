from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# TELECMI API CONFIG
TELECMI_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"
APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"

# Your audio file (uploaded in TeleCMI console)
AUDIO_FILE = "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav"

# Replace with your public Render URL
CALLBACK_URL = "https://ivr-calling-1nyf.onrender.com/handle_input"

@app.route('/make_call', methods=['GET'])
def make_call():
    """ Initiates outbound call and plays audio """
    data = {
        "appid": APP_ID,
        "secret": SECRET,
        "from": 917943446575,   # your registered TeleCMI number
        "to": 917775980069,     # recipient's number
        "extra_params": {"order_id": "ORD12345"},
        "pcmo": [
            {
                "action": "play",
                "file_name": AUDIO_FILE
            },
            {
                "action": "gather",
                "max_digits": 1,
                "timeout": 5,
                "callback_url": CALLBACK_URL
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(TELECMI_URL, json=data, headers=headers)

    if response.status_code == 200:
        return {"status": "✅ Outbound call started", "response": response.json()}
    else:
        return {"status": "❌ Failed", "code": response.status_code, "response": response.text}


@app.route('/handle_input', methods=['POST'])
def handle_input():
    """ Handles user DTMF input and replays audio """
    data = request.get_json()
    pressed = data.get("digits")
    print(f"User pressed: {pressed}")

    # We are just replaying the same audio regardless of input
    replay_audio = AUDIO_FILE

    response = {
        "pcmo": [
            {"action": "play", "file_name": replay_audio},
            {"action": "gather", "max_digits": 1, "timeout": 5, "callback_url": CALLBACK_URL}
        ]
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
