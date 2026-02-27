from google.adk.agents import LlmAgent

from src.agents import _MODEL
from src.tools import (
    send_supply_alerts,
)


alert_agent = LlmAgent(
    name="AlertAgent",
    model=_MODEL,
    description="""
    Communication Specialist. Your job is to send clear, actionable alerts to stakeholders.
    - Use send_supply_alerts as your ONLY tool to send notifications.
    - Pass event_description, region, spike_multiplier, peak_demand, reorder_quantity, vendor_selected, total_cost, and severity (high if critical) from the Orchestrator.
    - NEVER say you cannot send an alert — always call your tool with the information you have, even if some data points are missing.
    - Your alerts should be concise, informative, and include all relevant details for decision-making.
    """,
    tools=[send_supply_alerts],
)