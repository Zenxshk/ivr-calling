# app.py
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🎯 IVR System ACTIVE - Voice Ready"

@app.route('/call', methods=['POST'])
def handle_call():
    """Piopiy Answer URL - This gets called when someone answers"""
    try:
        data = request.json or {}
        user_input = data.get('dtmf', '')
        
        print("🔔 WEBHOOK CALLED - Call Answered!")
        print(f"User pressed: '{user_input}'")
        print(f"Full data: {data}")
        
        if user_input == '':
            # First interaction - Welcome message
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Hello! Welcome to our automated IVR system.</Speak>
    <GetInput maxDigits="1" timeout="10">
        <Speak>Press 1 for customer service, or press 2 for technical support</Speak>
    </GetInput>
</Response>"""
        
        elif user_input == '1':
            # User pressed 1
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>You selected customer service. Thank you for calling. Goodbye!</Speak>
    <Hangup/>
</Response>"""
        
        elif user_input == '2':
            # User pressed 2
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>You selected technical support. Our team will contact you shortly. Goodbye!</Speak>
    <Hangup/>
</Response>"""
        
        else:
            # Invalid input
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Invalid option selected. Thank you for calling. Goodbye!</Speak>
    <Hangup/>
</Response>"""
        
        print("✅ Sending VoiceXML response to Piopiy")
        return response_xml, 200, {'Content-Type': 'application/xml'}
    
    except Exception as e:
        print(f"❌ Error in webhook: {e}")
        # Fallback response
        error_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Thank you for your call. Have a great day!</Speak>
    <Hangup/>
</Response>"""
        return error_xml, 200, {'Content-Type': 'application/xml'}

@app.route('/event', methods=['POST'])
def handle_event():
    """Call events webhook"""
    data = request.json or {}
    print("📊 Call Event:", data)
    return {"status": "success"}

@app.route('/debug', methods=['POST'])
def handle_debug():
    """Debug webhook"""
    data = request.json or {}
    print("🐛 Debug Info:", data)
    return {"status": "success"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 IVR Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)