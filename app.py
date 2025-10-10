# app.py
import os
import pathlib
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response, send_from_directory

# Load .env if present
load_dotenv()

app = Flask(__name__, static_folder="static")

# -------------------------------
# Configuration (can override via .env)
# -------------------------------
# Your public app URL (where provider will POST the answer_url)
BASE_URL = os.getenv("BASE_URL", "https://ivr-calling-1nyf.onrender.com")

# Telecom / provider credentials (use env for production)
APP_ID = os.getenv("APP_ID", "4222424")
APP_SECRET = os.getenv("APP_SECRET", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")

# Provider endpoint (replace if your provider uses a different path)
# From your message: provider base is https://testing.com ; we append a likely API path.
PROVIDER_API = os.getenv("PROVIDER_API", "https://testing.com/v1/call")

# Numbers (E.164 format strongly recommended)
FROM_NUMBER = os.getenv("FROM_NUMBER", "+917943446575")   # virtual / caller number
TO_NUMBER = os.getenv("TO_NUMBER", "+917775980069")       # destination/customer number

DEFAULT_AUDIO = os.getenv("DEFAULT_AUDIO", "welcome.mp3")
SECOND_AUDIO = os.getenv("SECOND_AUDIO", "second.mp3")

# -------------------------------
# Helpers
# -------------------------------
def safe_static_path(filename):
    """Ensure path stays inside static folder to avoid directory traversal."""
    base = pathlib.Path(app.static_folder).resolve()
    candidate = (base / filename).resolve()
    if not str(candidate).startswith(str(base)):
        raise ValueError("Invalid path")
    return candidate

# -------------------------------
# Endpoint: Trigger outbound call
# -------------------------------
@app.route("/make-call", methods=["POST"])
def make_call():
    """
    Trigger an outbound call via the telephony provider.
    Accepts optional JSON fields to override 'from' and 'to':
      { "from": "...", "to": "..." }
    """
    # allow caller to override numbers in request JSON (optional)
    body = request.get_json(silent=True) or {}
    from_number = body.get("from", FROM_NUMBER)
    to_number = body.get("to", TO_NUMBER)

    # The URL the provider should call back to when the call is answered
    answer_url = f"{BASE_URL.rstrip('/')}/call"

    payload = {
        "from": from_number,
        "to": to_number,
        # many providers call this parameter 'answer_url' or 'callback_url' — check your provider docs
        "answer_url": answer_url,
    }

    # Header auth — your provider docs may require different auth (Bearer, Basic, etc.)
    headers = {
        "Content-Type": "application/json",
        "X-App-ID": APP_ID,
        "X-App-Secret": APP_SECRET,
    }

    try:
        # Make request to provider API to initiate the call
        res = requests.post(PROVIDER_API, json=payload, headers=headers, timeout=15)
        # Try to parse JSON response if possible:
        try:
            data = res.json()
        except ValueError:
            data = {"text_response": res.text}

        res.raise_for_status()
        return jsonify({"status": "success", "provider_response": data}), 200

    except requests.exceptions.RequestException as e:
        # include provider response text if available to help debugging
        message = str(e)
        try:
            provider_text = getattr(e.response, "text", None)
            if provider_text:
                message += f" | provider_response: {provider_text}"
        except Exception:
            pass
        return jsonify({"status": "error", "message": message}), 500

# -------------------------------
# Endpoint: IVR Flow (Answer URL)
# -------------------------------
@app.route("/call", methods=["POST", "GET"])
def handle_call():
    """
    This is the 'Answer URL' the provider will POST to when the call connects.
    It must return XML (or JSON) in whatever format your provider expects.
    The example below returns simple TwiML-like XML:
      - Plays welcome audio
      - Gathers single digit (1 digit) — provider should forward DTMF back to this same /call
    If your provider expects a different XML schema, adapt the response format accordingly.
    """
    # Providers frequently send DTMF digits in either "Digits" or "digits" param
    digits = request.values.get("Digits") or request.values.get("digits")

    if digits:
        # If user pressed 1 or 2, play second audio and hang up (example)
        if digits in ["1", "2"]:
            return ivr_response(SECOND_AUDIO, gather=False)
        else:
            # invalid input — replay default and gather again
            return ivr_response(DEFAULT_AUDIO, gather=True)

    # Initial connect — play welcome and collect 1 digit
    return ivr_response(DEFAULT_AUDIO, gather=True)

# -------------------------------
# Function: Generate IVR XML (TwiML-like)
# -------------------------------
def ivr_response(filename, gather=True):
    # validate file exists in static
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
# Endpoint: serve audio files from ./static
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
# Run
# -------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
