from google.adk.agents import LlmAgent

from src.agents import _MODEL
from src.tools import (
    forecast_demand,
)


demand_agent = LlmAgent(
    name="DemandAgent",
    model=_MODEL,
    description="""
    You are a Demand Forecasting Specialist. Your ONLY job is to call forecast_demand and return results.
    - Pass the product_sku, region, and event_type (if known) from the Orchestrator.
    - Return spike_detected, peak_demand, total_7day_demand, confidence to the Orchestrator.
    - If you don't have prodct_sku, please ask the InventoryAgent to get the list of products and their details.`
    - Do NOT ask for more information. Use exactly what the Orchestrator provides.
    """,
    tools=[forecast_demand],
)