import asyncio
import sys
import logging
import os
from dotenv import load_dotenv
from livekit.agents import llm, voice
from livekit.plugins import google, silero
from mem0 import MemoryClient
from tools import get_weather, search_web, send_email, search_knowledge_base
from reasoning_llm import NvidiaNIMLLM
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION

load_dotenv()

async def entrypoint(ctx):
    logger = logging.getLogger("assistant")
    logger.info(f"starting assistant for room {ctx.room.name}")
    
    memory_client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
    user_id = "default_user"

    try:
        memories = memory_client.get_all(user_id=user_id)
        memory_text = "\n".join([m['text'] for m in memories]) if memories else "No previous memories found."
    except Exception as e:
        logger.error(f"Failed to retrieve memories: {e}")
        memory_text = "No previous memories found (error retrieving)."
        
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(
        role="system",
        content=f"{AGENT_INSTRUCTION}\n\nUser Memory:\n{memory_text}",
    )

    agent = voice.Agent(
        vad=silero.VAD.load(),
        stt=google.STT(api_key=os.getenv("GOOGLE_API_KEY")),
        llm=NvidiaNIMLLM(model="deepseek-ai/deepseek-r1-distill-qwen-32b"),
        tts=google.TTS(api_key=os.getenv("GOOGLE_API_KEY")),
        chat_ctx=chat_ctx,
        tools=[get_weather, search_web, send_email, search_knowledge_base]
    )

    await ctx.connect(agent=agent)
    session = agent.session

    @ctx.room.on("data_received")
    def on_data_received(payload: bytes, participant, kind):
        import json
        try:
            data = json.loads(payload.decode())
            if data.get("type") == "chat":
                msg = data.get("message")
                logger.info(f"Received text chat from {participant.identity}: {msg}")
                
                # Add to agent's chat context so she knows what was said
                agent.chat_ctx.add_message(role="user", content=msg)
                
                # Trigger a response from the LLM specifically for text
                asyncio.create_task(send_text_response())
        except Exception as e:
            logger.error(f"Error handling data received: {e}")

    async def send_text_response():
        import json
        try:
            # We use the existing LLM to generate a text response
            # FRIDAY should respond in character
            stream = agent.llm.chat(chat_ctx=agent.chat_ctx)
            full_response = ""
            async for chunk in stream:
                content = None
                if hasattr(chunk, 'choices') and chunk.choices:
                    content = chunk.choices[0].delta.content
                elif hasattr(chunk, 'delta') and chunk.delta:
                    content = chunk.delta.content
                
                if content:
                    full_response += content
            
            # Publish the text response back to the room
            response_data = json.dumps({
                "type": "chat",
                "message": full_response,
                "sender": "FRIDAY"
            })
            await ctx.room.local_participant.publish_data(response_data.encode(), reliable=True)
            
            # Also add the AI response to the chat context
            agent.chat_ctx.add_message(role="assistant", content=full_response)
            
            # SPEAK the response
            await agent.session.say(full_response, allow_interruptions=True)
            
        except Exception as e:
            logger.error(f"Failed to send text response: {e}")

    @session.on("conversation_item_added")
    def on_conversation_item_added(event):
        if event.item.type == "message" and event.item.role == "user":
            content = event.item.text_content()
            if content:
                try:
                    memory_client.add([{"role": "user", "content": content}], user_id=user_id)
                except Exception as e:
                    logger.error(f"Failed to add memory: {e}")

    await session.say(SESSION_INSTRUCTION, allow_interruptions=True)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Create the loop before importing cli
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        from livekit.agents import WorkerOptions, cli
        logging.basicConfig(level=logging.INFO)
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
    finally:
        loop.close()
