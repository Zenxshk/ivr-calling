from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# 🔹 Example constants (replace with your real values)
APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"
FROM_NUMBER = "917943446575"
TO_NUMBER = "917775980069"

# === 1️⃣ MAIN API — Generate Play Input JSON ===
@app.route('/make_call', methods=['POST'])
def make_call():
    try:
        # Optionally take input from frontend
        data = request.get_json() or {}

        # If user provides new to/from, override defaults
        from_number = data.get("from", FROM_NUMBER)
        to_number = data.get("to", TO_NUMBER)
        file_name = data.get("file_name", "music_file.wav")

        # This will be your logic that Piopiy/GIMA expects
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
                    "max_digit": 4,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": " https://ivr-calling-1nyf.onrender.com/dtmf"  # Replace with your DTMF handling API
                }
            ]
        }

        return jsonify(payload), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 2️⃣ DTMF HANDLER — When user presses keys ===
@app.route('/dtmf', methods=['POST'])
def handle_dtmf():
    try:
        data = request.get_json()
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


# === Run the Flask app ===
if __name__ == "__main__":
    print("🚀 Flask Server Running — Ready for Piopiy JSON API Logic")
    app.run(host="0.0.0.0", port=5000, debug=True)
