from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# 🔹 TeleCMI API Endpoint
TELECMI_API_URL = "https://rest.telecmi.com/v2/ind_pcmo_make_call"

# 🔹 Your TeleCMI credentials
APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"
FROM_NUMBER = "917943446575"
TO_NUMBER = "917775980069"

# === 1️⃣ MAIN API — Make Actual Call to TeleCMI ===
@app.route('/make_call', methods=['POST', 'GET'])  # Added GET for testing
def make_call():
    try:
        # Optionally take input from frontend
        data = request.get_json() or {}
        
        # If user provides new to/from, override defaults
        from_number = data.get("from", FROM_NUMBER)
        to_number = data.get("to", TO_NUMBER)
        file_name = data.get("file_name", "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav")

        # TeleCMI expects form-data, not JSON
        payload = {
            "appid": APP_ID,
            "secret": SECRET,
            "from": from_number,
            "to": to_number,
            "extra_params": json.dumps({"order_id": "ORD12345"}),  # Note: stringified JSON
            "pcmo": json.dumps([  # Note: stringified JSON array
                {
                    "action": "play_get_input",
                    "file_name": file_name,
                    "max_digit": 4,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": "https://ivr-calling-1nyf.onrender.com/dtmf"  # Fixed space
                }
            ])
        }

        # 🔹 MAKE THE ACTUAL API CALL TO TELECMI
        response = requests.post(TELECMI_API_URL, data=payload)
        
        # Return TeleCMI's response
        return jsonify({
            "status": "success",
            "telecmi_response": response.json(),
            "status_code": response.status_code
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === 2️⃣ DTMF HANDLER — When user presses keys ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        data = request.get_json()
        print(f"📞 Received DTMF data: {data}")
        
        digit = data.get("digit", "")
        print(f"📞 User pressed: {digit}")

        # Logic for pressed key
        if digit == "1":
            next_action = {
                "action": "play",
                "file_name": "thank_you_1.wav"
            }
        elif digit == "2":
            next_action = {
                "action": "play",
                "file_name": "thank_you_2.wav"
            }
        else:
            next_action = {
                "action": "play",
                "file_name": "invalid_option.wav"
            }

        return jsonify(next_action), 200

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