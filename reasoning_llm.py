import os
import logging
from typing import Optional
from livekit.plugins import openai
from livekit.agents import llm

logger = logging.getLogger("reasoning_llm")

class OpenRouterLLM(openai.LLM):
    def __init__(
        self,
        model: str = "stepfun/step-3.5-flash:free",
        api_key: Optional[str] = None,
        base_url: str = "https://openrouter.ai/api/v1",
    ) -> None:
        super().__init__(
            model=model,
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
            base_url=base_url,
        )

class NvidiaNIMLLM(openai.LLM):
    def __init__(
        self,
        model: str = "deepseek-ai/deepseek-r1-distill-qwen-32b",
        api_key: Optional[str] = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
    ) -> None:
        # Note: Some NVIDIA models might need specific base URLs or configurations
        # but integrate.api.nvidia.com/v1 is the standard OpenAI-compatible endpoint.
        super().__init__(
            model=model,
            api_key=api_key or os.getenv("NVIDIA_API_KEY"),
            base_url=base_url,
        )
