# app.py - NEW FILE for IVR logic
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/call', methods=['POST'])
def handle_call():
    """This handles the call when answered"""
    try:
        data = request.json or {}
        user_input = data.get('dtmf', '')
        
        print(f"📞 Call received - User pressed: {user_input}")
        
        if user_input == '':
            # First interaction - welcome message
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Welcome to our service! Thank you for calling.</Speak>
    <GetInput maxDigits="1" timeout="10">
        <Speak>Press 1 for customer service. Press 2 for technical support.</Speak>
    </GetInput>
</Response>"""
        
        elif user_input == '1':
            # User pressed 1
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>You selected customer service. Our team will assist you shortly.</Speak>
    <Hangup/>
</Response>"""
        
        elif user_input == '2':
            # User pressed 2
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>You selected technical support. Please hold while we connect you.</Speak>
    <Hangup/>
</Response>"""
        
        else:
            # Invalid input
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Invalid option. Please try again.</Speak>
    <Redirect>https://your-app.onrender.com/call</Redirect>
</Response>"""
        
        return response_xml, 200, {'Content-Type': 'application/xml'}
    
    except Exception as e:
        print(f"Error: {e}")
        # Fallback response
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)