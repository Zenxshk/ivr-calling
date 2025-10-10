# call_trigger.py
from piopiy import RestClient, Action

def make_call():
    try:
        print("🚀 INITIATING PIOPIY CALL...")
        
        # Initialize exactly as per documentation - App ID and Secret
        piopiy = RestClient("4222424", "ccf0a102-ea6a-4f26-8d1c-7a1732eb0780")
        
        print(f"📞 To Number: 917775980069")
        print(f"📞 Caller ID: 917943446575")
        
        # Create PCMO actions for IVR
        action = Action()
        
        # Add webhook for DTMF input collection
        action.playGetInput(
            "https://ivr-calling-1nyf.onrender.com/call",  # Your webhook URL
            "",  # No audio file - use TTS
            {'max_digits': 1, 'max_retry': 2}
        )
        
        # Make the call with PCMO actions
        response = piopiy.voice.call(
            "917775980069",    # Destination number
            "917943446575",    # Caller ID
            action.PCMO(),     # PCMO actions with webhook
            {
                'duration': 120,
                'timeout': 30,
                'loop': 1
            }
        )
        
        print("✅ CALL INITIATED SUCCESSFULLY!")
        print("📋 Response:", response)
        return response
        
    except Exception as error:
        print(f"❌ CALL FAILED: {error}")
        return None

if __name__ == "__main__":
    result = make_call()
    if result:
        print("🎉 Call initiated! Phone should ring.")
    else:
        print("😞 Call failed.")