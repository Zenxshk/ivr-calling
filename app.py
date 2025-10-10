# app.py
import os
import pathlib
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder="static")

# Config
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
DEFAULT_AUDIO = os.getenv("DEFAULT_AUDIO", "welcome.mp3")
SECOND_AUDIO = os.getenv("SECOND_AUDIO", "second.mp3")

def safe_static_path(filename):
    base = pathlib.Path(app.static_folder).resolve()
    candidate = (base / filename).resolve()
    if not str(candidate).startswith(str(base)):
        raise ValueError("Invalid path")
    return candidate

def ivr_response(filename, gather=True):
    try:
        safe_static_path(filename)
    except Exception:
        filename = DEFAULT_AUDIO
    audio_url = f"{BASE_URL}/audio/{filename}"
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

@app.route("/call", methods=["POST", "GET"])
def handle_call():
    digits = request.values.get("Digits") or request.values.get("digits")
    if digits in ["1", "2"]:
        return ivr_response(SECOND_AUDIO, gather=False)
    return ivr_response(DEFAULT_AUDIO, gather=True)

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    try:
        safe_static_path(filename)
    except Exception:
        return Response("Invalid filename", status=400)
    return send_from_directory(app.static_folder, filename)

@app.route("/")
def index():
    return "IVR Flask Server Running"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
