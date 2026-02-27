import uvicorn
from fastapi import FastAPI

from ag_ui_adk import add_adk_fastapi_endpoint

from src.core.config import settings
from src.agents.factory import create_adk_agent

app = FastAPI(title=settings.app_name)

adk_supply_chain_agent = create_adk_agent()
add_adk_fastapi_endpoint(app, adk_supply_chain_agent, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
