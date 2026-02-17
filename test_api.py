import asyncio
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

async def test_simple():
    api_key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    payload = {
        "model": "stepfun/step-3.5-flash:free",
        "messages": [
            {"role": "user", "content": "How many r's are in the word 'strawberry'?"}
        ],
        "reasoning": {"enabled": True}
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    print("Sending request to OpenRouter...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        message = data['choices'][0]['message']
        print(f"Content: {message.get('content')}")
        print(f"Reasoning: {message.get('reasoning_details')}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    asyncio.run(test_simple())
