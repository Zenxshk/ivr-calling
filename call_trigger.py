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
TO_NUMBER = "919518337344"

# === 1️⃣ MAIN API — Make Actual Call to TeleCMI ===
@app.route('/make_call', methods=['POST', 'GET'])
def make_call():
    try:
        # Get data from request (accept both JSON and form-data)
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form.to_dict() or {}

        # If user provides new to/from, override defaults
        from_number = data.get("from", FROM_NUMBER)
        to_number = data.get("to", TO_NUMBER)
        file_name = data.get("file_name", "music_file.wav")

        # Prepare the EXACT payload that works in Postman
        payload = {
            "appid": APP_ID,
            "secret": SECRET,
            "from": int(from_number),  # Convert to integer like your working example
            "to": int(to_number),      # Convert to integer like your working example
            "extra_params": {"order_id": "ORD12345"},
            "pcmo": [
                {
                    "action": "play_get_input",
                    "file_name": file_name,
                    "max_digit": 1,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": "https://ivr-calling-1nyf.onrender.com/dtmf"
                }
            ]
        }

        # 🔹 MAKE THE ACTUAL API CALL TO TELECMI with JSON
        headers = {
            'Content-Type': 'application/json'
        }
        
        print(f"📞 Sending payload to TeleCMI: {json.dumps(payload, indent=2)}")
        
        response = requests.post(TELECMI_API_URL, json=payload, headers=headers)
        
        # Return the response
        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "message": "Call initiated successfully",
                "telecmi_response": response.json(),
                "status_code": response.status_code
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to initiate call",
                "telecmi_response": response.text,
                "status_code": response.status_code
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === 2️⃣ DTMF HANDLER — When user presses keys ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        # TeleCMI might send form-data to DTMF handler
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
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


# === 3️⃣ HOME ROUTE ===
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "✅ IVR Calling API is WORKING!",
        "endpoints": {
            "make_call": "POST /make_call",
            "dtmf_handler": "POST /dtmf"
        }
    })


# === 4️⃣ HEALTH CHECK ===
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Server is running!"})


if __name__ == "__main__":
    print("🚀 Flask Server Running — Ready for TeleCMI IVR Calls")
    app.run(host="0.0.0.0", port=5000, debug=True)