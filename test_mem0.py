import os
import asyncio
from mem0 import MemoryClient
from dotenv import load_dotenv

load_dotenv()

async def test_mem0():
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        print("MEM0_API_KEY not found in .env")
        return

    # Initialize Memory Client
    client = MemoryClient(api_key=api_key)

if __name__ == "__main__":
    import os
    from mem0 import MemoryClient
    api_key = os.getenv("MEM0_API_KEY")
    client = MemoryClient(api_key=api_key)
    
    user_id = "test_user_123"
    
    print("Adding a memory...")
    client.add([{"role": "user", "content": "I love the color blue."}], user_id=user_id)
    
    print("Retrieving memories...")
    memories = client.get_all(user_id=user_id)
    for m in memories:
        print(f"Memory: {m['text']}")

    print("Searching memories...")
    search_results = client.search("What color do I like?", user_id=user_id)
    for res in search_results:
        print(f"Search Result: {res['text']}")
