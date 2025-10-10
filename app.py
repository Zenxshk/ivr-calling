import os
import pathlib
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response, send_from_directory

# Load environment variables if needed
load_dotenv()

app = Flask(__name__, static_folder="static")

# Your credentials and numbers
BASE_URL = os.getenv("BASE_URL", "https://your-render-or-ngrok-url.com")  # Replace with your deployed URL
APP_ID = "4222424"
APP_SECRET = "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780"

FROM_NUMBER = "917943446575"   # your virtual number
TO_NUMBER = "7775980069"       # destination number

DEFAULT_AUDIO = "welcome.mp3"
SECOND_AUDIO = "second.mp3"

# -------------------------------
# Helper for safe static path
# -------------------------------
def safe_static_path(filename):
    base = pathlib.Path(app.static_folder).resolve()
    candidate = (base / filename).resolve()
    if not str(candidate).startswith(str(base)):
        raise ValueError("Invalid path")
    return candidate


# -------------------------------
# Endpoint: Outbound Call Trigger
# -------------------------------
@app.route("/make-call", methods=["POST"])
def make_call():
    """Trigger an outbound IVR call."""
    answer_url = f"{BASE_URL.rstrip('/')}/call"

    payload = {
        "from": FROM_NUMBER,
        "to": TO_NUMBER,
        "answer_url": answer_url
    }

    headers = {
        "Content-Type": "application/json",
        "X-App-ID": APP_ID,
        "X-App-Secret": APP_SECRET
    }

    # NOTE: Replace this URL with your actual telephony provider endpoint (e.g., Exotel, Plivo, Twilio, etc.)
    api_url = "https://api.yourtelephonyprovider.com/v1/call"

    try:
        res = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        return jsonify({"status": "success", "data": res.json()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# Endpoint: IVR Flow (Answer URL)
# -------------------------------
@app.route("/call", methods=["POST", "GET"])
def handle_call():
    """
    Telephony provider will hit this URL when the call connects or
    when digits are pressed (DTMF input).
    """
    digits = request.values.get("Digits") or request.values.get("digits")

    # When user presses 1 or 2
    if digits:
        if digits in ["1", "2"]:
            return ivr_response(SECOND_AUDIO, gather=False)
        else:
            return ivr_response(DEFAULT_AUDIO, gather=True)

    # Initial call connect — play welcome.mp3 and wait for input
    return ivr_response(DEFAULT_AUDIO, gather=True)


# -------------------------------
# Function: Generate IVR XML
# -------------------------------
def ivr_response(filename, gather=True):
    try:
        safe_static_path(filename)
    except Exception:
        filename = DEFAULT_AUDIO

    base = BASE_URL.rstrip("/")
    audio_url = f"{base}/audio/{filename}"

    if gather:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
    <Gather numDigits="1" action="/call" method="POST" timeout="5" />
</Response>"""
    else:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
    <Hangup/>
</Response>"""

    return Response(xml, mimetype="text/xml")


# -------------------------------
# Endpoint: Serve audio files
# -------------------------------
@app.route("/audio/<path:filename>")
def serve_audio(filename):
    try:
        safe_static_path(filename)
    except Exception:
        return Response("Invalid filename", status=400)
    return send_from_directory(app.static_folder, filename)


# -------------------------------
# Root endpoint
# -------------------------------
@app.route("/")
def index():
    return "IVR Flask Server Running"


# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
