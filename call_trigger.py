import os
from flask import Flask, jsonify, request
import json
import logging

app = Flask(__name__)

from flask_cors import CORS

CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging to flow into Gunicorn/Render logs
_gunicorn_logger = logging.getLogger('gunicorn.error')
if _gunicorn_logger.handlers:
    app.logger.handlers = _gunicorn_logger.handlers
    app.logger.setLevel(_gunicorn_logger.level)
app.logger.propagate = False

# 🔹 Config (prefer environment variables on Render)
APP_ID = int(os.environ.get("APP_ID", "4222424"))
SECRET = os.environ.get("SECRET", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")
FROM_NUMBER = os.environ.get("FROM_NUMBER", "917943446565")
TO_NUMBER = os.environ.get("TO_NUMBER", "919518337344")

# CDN file keys from your TeleCMI portal (2.png -> key Name column)
FILE_KEY_1 = os.environ.get("FILE_KEY_1", "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav")
FILE_KEY_2 = os.environ.get("FILE_KEY_2", "1760362929284ElevenLabs20251009T151214AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6a456e30-a83a-11f0-9f7b-3b2ce86cca8b_piopiy.wav")

# === 1️⃣ MAIN API — Generate Play Input JSON ===
@app.route('/make_call', methods=['POST'])
def make_call():
    try:
        data = request.get_json() or {}

        from_number = data.get("from", FROM_NUMBER)
        to_number = data.get("to", TO_NUMBER)
        file_name = data.get("file_name", FILE_KEY_1)

        # ✅ Ensure numeric
        from_number = int(from_number)
        to_number = int(to_number)

        action_url = request.url_root.rstrip("/") + "/dtmf"
        payload = {
            "appid": APP_ID,
            "secret": SECRET,
            "from": from_number,
            "to": to_number,
            "extra_params": {"order_id": "ORD12345"},
            "pcmo": [
                {
                    "action": "play_get_input",
                    "file_name": file_name,
                    "max_digit": 1,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": action_url
                }
            ]
        }

        # ✅ Send to TeleCMI directly here:
        telecmi_url = "https://rest.telecmi.com/v2/ind_pcmo_make_call"
        import requests
        res = requests.post(telecmi_url, json=payload, timeout=10)
        return jsonify({
            "status": "success",
            "telecmi_response": res.json(),
            "status_code": res.status_code
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 2️⃣ Inbound Answer URL — Return initial PCMO (screenshot 1 shows /call)
@app.route('/call', methods=['POST'])
def answer_call():
    try:
        action_url = request.url_root.rstrip("/") + "/dtmf"
        return jsonify([
            {
                "action": "play_get_input",
                "file_name": FILE_KEY_1,
                "max_digit": 1,
                "max_retry": 2,
                "timeout": 10,
                "action_url": action_url
            }
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 3️⃣ DTMF HANDLER — When user presses keys ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        data = request.get_json() or {}
        digit = str(data.get("digit", "")).strip()

        # Replace with your actual uploaded file keys from TeleCMI dashboard
        FILE_KEY_1 = "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav"
        FILE_KEY_2 = "1760362929284ElevenLabs20251009T151214AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6a456e30-a83a-11f0-9f7b-3b2ce86cca8b_piopiy.wav"
        FILE_KEY_INVALID = FILE_KEY_1  # repeat the main prompt if input invalid

        if digit == "1":
            actions = [
                {"action": "clear"},
                {"action": "play", "file_name": FILE_KEY_2}
            ]
        elif digit == "2":
            actions = [
                {"action": "clear"},
                {"action": "play", "file_name": FILE_KEY_1}
            ]
        else:
            # Invalid or empty input: replay prompt
            actions = [
                {
                    "action": "play_get_input",
                    "file_name": FILE_KEY_INVALID,
                    "max_digit": 1,
                    "max_retry": 1,
                    "timeout": 10,
                    "action_url": "https://ivr-calling-1nyf.onrender.com/dtmf"
                }
            ]

        return jsonify(actions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Health and index ===
@app.route('/', methods=['GET'])
def index():
    return "IVR service running", 200

@app.route('/healthz', methods=['GET'])
def healthz():
    return "ok", 200


# === Run the Flask app ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.logger.info("🚀 Flask Server Running — Ready for Piopiy JSON API Logic")
    app.run(host="0.0.0.0", port=port, debug=False)
