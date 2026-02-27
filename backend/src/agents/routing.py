from google.adk.agents import LlmAgent

from src.agents import _MODEL
from src.tools import (
    plan_delivery_route,
)


routing_agent = LlmAgent(
    name="RoutingAgent",
    model=_MODEL,
    description="""
    You are a Logistics Specialist. Your job is to plan delivery routes for inventory transfers or supplier shipments.
    - Use plan_delivery_route when inventory_agent reports transfers are needed.
    - Pass the list of transfers (from_warehouse, to_warehouse, quantity, distance_km) and urgency (high if critical) from the Orchestrator.
    - Return transport_mode (truck, express, train), estimated_delivery_time_hours, and cost to the Orchestrator.
    """,
    tools=[plan_delivery_route],
)
