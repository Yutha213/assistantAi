import asyncio
import os
from dotenv import load_dotenv
from reasoning_llm import NvidiaNIMLLM
from livekit.agents import llm

async def test_llm():
    load_dotenv()
    print("Testing NvidiaNIMLLM...")
    
    llm_instance = NvidiaNIMLLM(model="deepseek-ai/deepseek-r1-distill-qwen-32b")
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(role="user", content="Hello, who are you?")
    
    try:
        stream = llm_instance.chat(chat_ctx=chat_ctx)
        print("Response: ", end="")
        async for chunk in stream:
            if chunk.delta.content:
                print(chunk.delta.content, end="", flush=True)
        print("\nTest successful!")
    except Exception as e:
        print(f"\nTest failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm())
