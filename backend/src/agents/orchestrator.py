from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext

from src.utils.state import SupplyChainState
from . import _MODEL
from src.agents.demand import demand_agent
from src.agents.inventory import inventory_agent
from src.agents.vendor import vendor_agent
from src.agents.routing import routing_agent
from src.agents.alert import alert_agent


def before_orchestrator(callback_context: CallbackContext):
    if "workflow_state" not in callback_context.state:
        callback_context.state["workflow_state"] = SupplyChainState().dict()


orchestrator = LlmAgent(
    name="SupplyChainOrchestrator",
    model=_MODEL,
    description="""
    Master Orchestrator for supply chain management. You coordinate 5 specialists:
      - DemandAgent: forecasts demand spikes and trends using various data sources
      - InventoryAgent: monitors stock levels, identifies gaps, and determines if reordering or transfers are needed and product based information.
      - VendorAgent: negotiates with suppliers for replenishment when inventory gaps are identified
      - RoutingAgent: plans delivery routes for inventory transfers or supplier shipments when needed
      - AlertAgent: sends notifications to stakeholders if critical issues or demand spikes are detected

    RULES:
    1. NEVER say "I cannot" — always delegate to the right specialist.
    2. Full workflow order: DemandAgent → InventoryAgent → VendorAgent (if reorder needed)
       → RoutingAgent (if transfers exist) → AlertAgent.
    3. Pass data explicitly between agents — tell each one what the previous found.
    4. End with a clear, actionable summary of all decisions made.
    5. Don't call AlertAgent without first trying to resolve with VendorAgent or RoutingAgent. Alert only if it's critical or you have no other choice.
    """,
    sub_agents=[
        demand_agent,
        inventory_agent,
        vendor_agent,
        routing_agent,
        alert_agent,
    ],
    before_agent_callback=before_orchestrator,
)
