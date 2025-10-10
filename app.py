# app.py
from flask import Flask, request, Response
import pyttsx3
import os
import threading
import tempfile

app = Flask(__name__)

def text_to_speech(text, filename):
    """Convert text to speech and save as MP3"""
    try:
        engine = pyttsx3.init()
        
        # Set voice properties
        engine.setProperty('rate', 150)    # Speed
        engine.setProperty('volume', 0.9)  # Volume
        
        # Get available voices
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)  # Use first voice
        
        # Save to file
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

@app.route('/')
def home():
    return "IVR System Running"

@app.route('/call', methods=['POST'])
def handle_call():
    """Piopiy Answer URL - Voice enabled"""
    try:
        data = request.json or {}
        user_input = data.get('dtmf', '')
        
        print(f"📞 Call received - User pressed: {user_input}")
        
        # Your Render app URL
        BASE_URL = "https://ivr-calling-1nyf.onrender.com"
        
        if user_input == '':
            # Welcome message
            welcome_text = "Welcome to our IVR system. Press 1 for services. Press 2 for support."
            
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>{welcome_text}</Speak>
    <GetInput maxDigits="1" timeout="10">
        <Speak>Please press 1 or 2</Speak>
    </GetInput>
</Response>"""
        
        elif user_input == '1':
            # Option 1 selected
            option1_text = "You selected services. Thank you for calling. Goodbye."
            
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>{option1_text}</Speak>
    <Hangup/>
</Response>"""
        
        elif user_input == '2':
            # Option 2 selected
            option2_text = "You selected support. Our team will contact you soon. Goodbye."
            
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>{option2_text}</Speak>
    <Hangup/>
</Response>"""
        
        else:
            # Invalid input
            invalid_text = "Invalid option. Please try again."
            
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>{invalid_text}</Speak>
    <Redirect>{BASE_URL}/call</Redirect>
</Response>"""
        
        print("✅ Sending VoiceXML response")
        return response_xml, 200, {'Content-Type': 'application/xml'}
    
    except Exception as e:
        print(f"Error: {e}")
        # Fallback with simple text
        error_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Welcome to our service. Thank you for calling.</Speak>
    <Hangup/>
</Response>"""
        return error_xml, 200, {'Content-Type': 'application/xml'}

@app.route('/event', methods=['POST'])
def handle_event():
    """Handle call events"""
    data = request.json or {}
    print("📊 Call event:", data)
    return {"status": "success"}

# Text-to-speech endpoint (optional)
@app.route('/tts/<text>')
def generate_tts(text):
    """Generate TTS audio for text"""
    try:
        filename = f"static/tts_{hash(text)}.mp3"
        if text_to_speech(text, filename):
            return {"status": "success", "file": filename}
        else:
            return {"status": "error"}, 500
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)