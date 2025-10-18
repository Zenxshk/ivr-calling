from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Piopiy API configuration
PIOPIY_BASE_URL = "https://api.telecmi.com/v1/call"
APP_ID = 4222424
SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"

@app.route('/')
def home():
    return jsonify({"message": "Piopiy Voice Call API Server"})

# Endpoint to initiate a voice call with play_get_input
@app.route('/api/make-call', methods=['POST'])
def make_call():
    """
    Initiate a voice call with play_get_input action
    Based on: https://doc.telecmi.com/piopiy/docs/play-file
    """
    try:
        # Get request data or use default
        data = request.get_json() or {
            "appid": APP_ID,
            "secret": SECRET,
            "from": 917943446575,
            "to": 917775980069,
            "extra_params": {"order_id": "ORD12345"},
            "pcmo": [
                {
                    "action": "play_get_input",
                    "file_name": "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav",
                    "max_digit": 1,
                    "max_retry": 2,
                    "timeout": 10,
                    "action_url": "https://your-webhook-url.com/webhook/input"
                }
            ]
        }

        # Make request to Piopiy API
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            PIOPIY_BASE_URL,
            json=data,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "status": "success",
                "message": "Call initiated successfully",
                "piopiy_response": result
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to initiate call",
                "error": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Webhook endpoint to receive user input from play_get_input
@app.route('/webhook/input', methods=['POST'])
def handle_user_input():
    """
    Webhook to receive user input from play_get_input action
    This URL should be set in the action_url field
    """
    try:
        data = request.get_json()
        
        # Log the received data
        print("Received user input:", data)
        
        # Process the user input
        if data:
            user_input = data.get('data', {}).get('digits')
            call_id = data.get('cid')
            
            # Here you can process the user input
            # For example: validate, store in database, trigger other actions
            
            return jsonify({
                "status": "success",
                "message": "Input received",
                "user_input": user_input,
                "call_id": call_id
            }), 200
        
        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    except Exception as e:
        print("Webhook error:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Endpoint for different PCMO actions
@app.route('/api/call-with-multiple-actions', methods=['POST'])
def call_with_multiple_actions():
    """
    Example with multiple PCMO actions
    """
    data = {
        "appid": APP_ID,
        "secret": SECRET,
        "from": 917943446575,
        "to": 917775980069,
        "extra_params": {"order_id": "ORD12345"},
        "pcmo": [
            {
                "action": "play",
                "file_name": "1760350048331ElevenLabs20251009T151503AnikaSweetLivelyHindiSocialMediaVoicepvcsp99s100sb100se0bm2wav6ca049c0-a81c-11f0-9f7b-3b2ce86cca8b_piopiy.wav"
            },
            {
                "action": "play_get_input",
                "file_name": "press-1-for-sales.wav",
                "max_digit": 1,
                "max_retry": 2,
                "timeout": 10,
                "action_url": "https://your-webhook-url.com/webhook/input"
            }
        ]
    }

    response = requests.post(PIOPIY_BASE_URL, json=data)
    return jsonify(response.json())

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Piopiy Voice Call API"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)