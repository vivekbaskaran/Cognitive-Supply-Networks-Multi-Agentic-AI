from ag_ui_adk import ADKAgent
from src.agents.orchestrator import orchestrator
from src.core.config import settings


def create_adk_agent() -> ADKAgent:
    return ADKAgent(
        adk_agent=orchestrator,
        user_id=settings.default_user,
        session_timeout_seconds=settings.session_timeout,
        use_in_memory_services=settings.use_in_memory,
    )