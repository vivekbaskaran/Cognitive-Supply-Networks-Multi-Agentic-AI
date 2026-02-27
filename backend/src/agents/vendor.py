from google.adk.agents import LlmAgent

from src.agents import _MODEL
from src.tools import (
    negotiate_with_vendor
)


vendor_agent = LlmAgent(
    name="VendorAgent",
    model=_MODEL,
    description="""
    Sourcing Specialist. Your job is to negotiate with suppliers and generate POs.
    - Use negotiate_with_vendor when inventory_agent reports reorder_needed = True.
    - Pass product_sku, quantity (use reorder_quantity), and urgency (high if critical) from the Orchestrator.
    - Return vendor_selected, price_per_unit, total_cost, and lead_time_days to the Orchestrator.
    - If you don't have the optimal vendors, Please check with the RoutingAgent to find out if there are nearby warehouses that can transfer stock faster than suppliers can deliver.
    """,
    tools=[negotiate_with_vendor],
)