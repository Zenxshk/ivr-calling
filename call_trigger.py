# call_trigger.py
from piopiy import RestClient

def make_call():
    try:
        print("🚀 INITIATING PIOPIY CALL...")
        
        # Initialize Piopiy client with your credentials
        piopiy = RestClient("4222424", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")
        
        # Your Render app URL
        answer_url = "https://ivr-calling-1nyf.onrender.com/call"
        
        print(f"📞 Calling: 917775980069")
        print(f"🎯 From: 917943446575") 
        print(f"🔗 Webhook: {answer_url}")
        
        # Make the call using Piopiy SDK
        response = piopiy.voice.call(
            "917775980069",    # to number
            "917943446575",    # from number (caller ID)
            answer_url,        # webhook URL for voice handling
            {
                'duration': 120,   # Max call duration
                'timeout': 30,     # Answer timeout
                'loop': 1          # Retry attempts
            }
        )
        
        print("✅ CALL INITIATED SUCCESSFULLY!")
        print("📋 Response Details:")
        print(f"   - Status: {response.get('status', 'Unknown')}")
        print(f"   - Call ID: {response.get('uuid', 'Unknown')}")
        print(f"   - Message: {response.get('message', 'Call ringing')}")
        
        return response
        
    except Exception as error:
        print(f"❌ CALL FAILED: {error}")
        return None

if __name__ == "__main__":
    result = make_call()
    if result:
        print("🎉 Phone should be ringing NOW! Check your phone.")
    else:
        print("😞 Call failed. Check the error above.")