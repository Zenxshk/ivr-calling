from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # CORS ENABLED

# 🔹 TeleCMI API Endpoint
TELECMI_API_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"

# 🔹 Your TeleCMI credentials
APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"
FROM_NUMBER = 917943446565   # ← no quotes → integer
TO_NUMBER = 917756043094     # ← no quotes → integer

# === 1️⃣ MAIN API — Make Actual Call to TeleCMI ===
@app.route('/make_call', methods=['POST', 'GET'])
def make_call():
    try:
        data = request.get_json() or {}
        
        # CONVERT TO INTEGERS (TeleCMI requires numbers)
        from_number = int(data.get("from", FROM_NUMBER))   # ← int()
        to_number = int(data.get("to", TO_NUMBER))         # ← int()

        file_name = data.get("file_name", "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav")

        payload = {
            "appid": APP_ID,
            "secret": SECRET,
            "from": from_number,        # ← now a number
            "to": to_number,            # ← now a number
            "extra_params": json.dumps({"order_id": "ORD12345"}),
            "pcmo": json.dumps([
                {
                    "action": "play_get_input",
                    "file_name": file_name,
                    "max_digit": 4,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": "https://ivr-calling-1nyf.onrender.com/dtmf"
                }
            ])
        }

        response = requests.post(TELECMI_API_URL, data=payload)
        response.raise_for_status()

        return jsonify({
            "status": "success",
            "telecmi_response": response.json(),
            "status_code": response.status_code
        }), 200

    except ValueError as e:
        return jsonify({"error": "Invalid phone number format. Must be digits only."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 2️⃣ DTMF HANDLER — When user presses keys ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        data = request.get_json()
        print(f"Received DTMF data: {data}")
        
        digit = data.get("digit", "")
        print(f"User pressed: {digit}")

        # Return as ARRAY to match TeleCMI spec
        if digit == "1":
            actions = [{"action": "play", "file_name": "thank_you_1.wav"}]
        elif digit == "2":
            actions = [{"action": "play", "file_name": "thank_you_2.wav"}]
        else:
            actions = [{"action": "play", "file_name": "invalid_option.wav"}]

        return jsonify(actions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# === 3️⃣ HOME ROUTE FOR TESTING ===
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "✅ IVR Calling API is WORKING!",
        "endpoints": {
            "make_call": "POST /make_call",
            "dtmf_handler": "POST /dtmf", 
            "health": "GET /health"
        }
    })


# === 4️⃣ HEALTH CHECK ===
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Server is running!"})


# === Run the Flask app ===
if __name__ == "__main__":
    print("🚀 Flask Server Running — Ready for TeleCMI IVR Calls")
    app.run(host="0.0.0.0", port=5000, debug=True)