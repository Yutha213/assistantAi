import time
import os
from livekit import api
from dotenv import load_dotenv

def generate_token(room_name, participant_name):
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv('LIVEKIT_API_KEY')
    api_secret = os.getenv('LIVEKIT_API_SECRET')
    
    if not api_key or not api_secret:
        print("Error: LIVEKIT_API_KEY or LIVEKIT_API_SECRET not found in .env file")
        return None

    # Create a token
    token = api.AccessToken(api_key, api_secret) \
        .with_identity(participant_name) \
        .with_name(participant_name) \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
        )) \
        .with_metadata("expert-ai-user")
        
    return token.to_jwt()

if __name__ == "__main__":
    import sys
    
    # Default values
    room = "my-expert-room"
    user = "User1"
    
    # Allow command line overrides
    if len(sys.argv) > 1:
        room = sys.argv[1]
    if len(sys.argv) > 2:
        user = sys.argv[2]
        
    print(f"\n--- Expert AI Token Generator ---")
    print(f"Room: {room}")
    print(f"User: {user}")
    
    jwt = generate_token(room, user)
    
    if jwt:
        print("\nYour Participant Token is:\n")
        print(jwt)
        print("\n---------------------------------\n")
        print("Copy the long string above and paste it into the 'Participant Token' field in index.html")
