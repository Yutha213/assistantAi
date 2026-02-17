import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_nvidia():
    api_key = os.getenv("NVIDIA_API_KEY")
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-ai/deepseek-r1-distill-qwen-32b",
        "messages": [{"role": "user", "content": "Hello, who are you?"}],
        "max_tokens": 100
    }
    
    try:
        print("Testing NVIDIA NIM DeepSeek-R1...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Success!")
        print(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(e.response.text)

if __name__ == "__main__":
    test_nvidia()
