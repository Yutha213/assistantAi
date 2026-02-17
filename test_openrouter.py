import asyncio
import os
from dotenv import load_dotenv
from reasoning_llm import OpenRouterLLM
from livekit.agents import llm
import logging

load_dotenv()

async def test_llm():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize LLM
    model = OpenRouterLLM()
    
    # Create chat context
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(
        llm.ChatMessage(
            role="user",
            content="How many r's are in the word 'strawberry'?",
        )
    )
    
    print("Sending request to OpenRouter...")
    
    # Get stream
    stream = model.chat(chat_ctx=chat_ctx)
    
    print("Response:")
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print("\n\nTest complete.")

if __name__ == "__main__":
    asyncio.run(test_llm())
