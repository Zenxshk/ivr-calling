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
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form.to_dict() or {}

        from_number = data.get("from", FROM_NUMBER)
        to_number = data.get("to", TO_NUMBER)
        file_name = data.get("file_name", "music_file.wav")

        payload = {
            "appid": APP_ID,
            "secret": SECRET,
            "from": int(from_number),
            "to": int(to_number),
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

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        print("📞 Sending Payload to TeleCMI:\n", json.dumps(payload, indent=2))

        # ✅ Force send JSON body as string (not auto-encoded)
        response = requests.post(TELECMI_API_URL, data=json.dumps(payload), headers=headers)

        return jsonify({
            "status": "success" if response.ok else "error",
            "telecmi_status_code": response.status_code,
            "telecmi_response": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === 2️⃣ DTMF HANDLER ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        print(f"📞 Received DTMF data: {data}")
        digit = data.get("dtmf") or data.get("digit", "")

        # logic for pressed key
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


# === HEALTH CHECK ===
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Server is running!"})


if __name__ == "__main__":
    print("🚀 Flask Server Running — Ready for TeleCMI IVR Calls")
    app.run(host="0.0.0.0", port=5000, debug=True)
