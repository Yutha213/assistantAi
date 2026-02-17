import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def list_models():
    api_key = os.getenv("NVIDIA_API_KEY")
    url = "https://integrate.api.nvidia.com/v1/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    
    try:
        print("Listing NVIDIA NIM Models...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        models = response.json()
        for model in models['data']:
            print(f"- {model['id']}")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(e.response.text)

if __name__ == "__main__":
    list_models()
