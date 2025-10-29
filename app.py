from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# === CONFIG ===
TELECMI_API_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"

APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"
FROM_NUMBER = 917943446565


# === ROUTE ===
@app.route('/make_call', methods=['POST', 'GET'])
def make_call():
    try:
        data = request.get_json() or {}
        
        # Get from/to — REQUIRED from frontend
        from_number = data.get("from")
        to_number = data.get("to")

        if not from_number or not to_number:
            return jsonify({"error": "Both 'from' and 'to' are required"}), 400

        try:
            from_number = int(from_number)
            to_number = int(to_number)
        except ValueError:
            return jsonify({"error": "Phone numbers must be digits only"}), 400

        file_name = data.get("file_name", "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav")

        payload = {
            "appid": APP_ID,
            "secret": SECRET,
            "from": from_number,
            "to": to_number,
            "extra_params": json.dumps({"order_id": "ORD12345"}),
            "pcmo": json.dumps([
                {
                    "action": "play_get_input",
                    "file_name": file_name,
                    "max_digit": 1,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": "https://ivr-calling-1nyf.onrender.com/dtmf"
                }
            ])
        }

        response = requests.post(TELECMI_API_URL, data=payload, timeout=10)
        
        return jsonify({
            "status": "success",
            "telecmi_response": response.json(),
            "status_code": response.status_code
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"TeleCMI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === DTMF ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        data = request.get_json() or {}
        digit = str(data.get("digit", "")).strip()

        if digit == "1":
            return jsonify([{"action": "play", "file_name": "thank_you_1.wav"}]), 200
        elif digit == "2":
            return jsonify([{"action": "play", "file_name": "thank_you_2.wav"}]), 200
        else:
            return jsonify([{"action": "play", "file_name": "invalid_option.wav"}]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "IVR API Ready"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)