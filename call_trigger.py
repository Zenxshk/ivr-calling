from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return jsonify({
            "message": "✅ Render Deployment is WORKING!",
            "status": "success", 
            "endpoint": "https://ivr-calling-1nyf.onrender.com/",
            "timestamp": "2024-01-01 12:00:00",
            "instructions": "Send a POST request with JSON data to test webhook functionality"
        })
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            return jsonify({
                "message": "✅ POST request received successfully!",
                "your_data": data,
                "status": "success",
                "response": "This is a test response from your deployed API"
            })
        except:
            return jsonify({
                "message": "❌ Error processing JSON data",
                "status": "error"
            }), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy 🟢",
        "message": "Server is running perfectly!",
        "deployment": "Active"
    })

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return jsonify({
            "message": "Test endpoint is working!",
            "try_post": "Send a POST request to this endpoint with any JSON data"
        })
    
    if request.method == 'POST':
        data = request.get_json() or {}
        return jsonify({
            "echo": "✅ Your data was received!",
            "received_data": data,
            "server_response": "Webhook is ready for Piopiy calls!"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)