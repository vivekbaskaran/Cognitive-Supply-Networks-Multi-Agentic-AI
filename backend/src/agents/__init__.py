import os
from src.core.config import settings
from google.adk.models.lite_llm import LiteLlm

GEMINI_MODEL = "gemini-2.5-flash-lite" # INFO: Switch this provider If you have Gemini Subscription, Or Free Access.
OPENAI_MODEL = LiteLlm(model="openai/gpt-4o-mini", temperature=0.2) # INFO: OpenAI Only providing the LLM Service with Payment.

_MODEL = GEMINI_MODEL if settings.provider == "google" else OPENAI_MODEL
os.environ["GOOGLE_API_KEY"] = settings.google_api_key
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

__all__ = [
    "_MODEL",
]