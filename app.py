# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/call', methods=['POST'])
def handle_call():
    """Handle incoming call webhook from Piopiy"""
    data = request.json
    print("Received call webhook:", data)
    
    # Return XML response for call handling
    response_xml = """
    <Response>
        <Speak>Hello! This is a test call from Piopiy.</Speak>
        <Hangup/>
    </Response>
    """
    
    return response_xml, 200, {'Content-Type': 'application/xml'}

@app.route('/event', methods=['POST'])
def handle_event():
    """Handle call events (CDR) from Piopiy"""
    data = request.json
    print("Received event:", data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)