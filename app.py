# app.py
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "IVR System Running"

@app.route('/call', methods=['POST'])
def handle_call():
    """Piopiy Answer URL - Called when call is answered"""
    try:
        data = request.json or {}
        print("📞 Call received")
        
        # Get user input if any
        user_input = data.get('dtmf', '')
        
        # Your Render app URL - UPDATE THIS
        BASE_URL = "https://ivr-calling-1nyf.onrender.com"
        
        if user_input == '':
            # First interaction - play welcome.mp3 and ask for input
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{BASE_URL}/static/welcome.mp3</Play>
    <GetInput maxDigits="1" timeout="10">
        <Speak>Press 1 or 2 to continue</Speak>
    </GetInput>
</Response>"""
        
        elif user_input in ['1', '2']:
            # User pressed 1 or 2 - play second.mp3 and hangup
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{BASE_URL}/static/second.mp3</Play>
    <Hangup/>
</Response>"""
        
        else:
            # Invalid input - play welcome.mp3 again
            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{BASE_URL}/static/welcome.mp3</Play>
    <Hangup/>
</Response>"""
        
        return response_xml, 200, {'Content-Type': 'application/xml'}
    
    except Exception as e:
        print(f"Error: {e}")
        # Fallback response
        BASE_URL = "https://ivr-calling-1nyf.onrender.com"
        error_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{BASE_URL}/static/welcome.mp3</Play>
    <Hangup/>
</Response>"""
        return error_xml, 200, {'Content-Type': 'application/xml'}

@app.route('/event', methods=['POST'])
def handle_event():
    """Piopiy Event URL"""
    data = request.json or {}
    print("📊 Event:", data)
    return {"status": "success"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)