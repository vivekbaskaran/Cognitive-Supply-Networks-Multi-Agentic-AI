from typing import Optional
from google.adk.tools import ToolContext
import datetime

from .vendor import VendorAgent
from .demand import DemandAgent
from .inventory import InventoryAgent
from .routing import RoutingAgent
from .alert import AlertAgent
from src.utils.state import SupplyChainState


def _get_state(tool_context: ToolContext) -> dict:
    state = tool_context.state.get("workflow_state")

    if state is None:
        state = SupplyChainState().dict()
        tool_context.state["workflow_state"] = state

    if "execution_trace" not in state:
        state["execution_trace"] = []

    return state


def _track(
    tool_context: ToolContext,
    tool_name: str,
    input_data: dict,
    result: dict,
):
    state = _get_state(tool_context)

    state["execution_trace"].append(
        {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "agent": tool_context.agent_name,
            "tool": tool_name,
            "input": input_data,
            "output": result,
        }
    )

    tool_context.state["workflow_state"] = state


_demand_svc = DemandAgent(demo_mode=True)
_inventory_svc = InventoryAgent(demo_mode=True)
_vendor_svc = VendorAgent(demo_mode=True)
_routing_svc = RoutingAgent(demo_mode=True)
_alert_svc = AlertAgent(demo_mode=True)


async def forecast_demand(
    tool_context: ToolContext,
    product_sku: str,
    region: str,
    event_type: Optional[str] = None,
) -> dict:
    """
    Forecast product demand for the next 7 days using weather forecasts,
    social media trends, and historical sales data.
    Returns spike_detected, peak_demand, total_7day_demand, and confidence score.

    Args:
        product_sku: Product SKU.
        region: Target region — Mumbai | Delhi | Bangalore | Chennai | Kolkata
        event_type: Demand driver — cyclone | cold_wave | festival | monsoon  (omit if none)
    """
    result = await _demand_svc.forecast_demand(product_sku, region, event_type)

    state = _get_state(tool_context)
    state.update(
        {
            "product_sku": product_sku,
            "region": region,
            "event_type": event_type,
            **result,
        }
    )

    tool_context.state["workflow_state"] = state
    _track(
        tool_context,
        "forecast_demand",
        {
            "product_sku": product_sku,
            "region": region,
            "event_type": event_type,
        },
        result,
    )

    return result


async def optimize_inventory(
    tool_context: ToolContext, product_sku: str, region: str, forecasted_demand: int
) -> dict:
    """
    Check current inventory across all warehouses, identify stock gaps vs
    forecasted demand, and plan inter-warehouse transfers.
    Call this AFTER forecast_demand.

    Args:
        product_sku: Product SKU to check
        region: Target region — Mumbai | Delhi | Bangalore | Chennai | Kolkata
        forecasted_demand: Demand quantity from forecast_demand (use total_7day_demand)
    """
    result = await _inventory_svc.optimize_inventory(
        product_sku, region, forecasted_demand
    )
    state = _get_state(tool_context)
    state.update(result)

    tool_context.state["workflow_state"] = state
    _track(
        tool_context,
        "optimize_inventory",
        {
            "product_sku": product_sku,
            "region": region,
            "forecasted_demand": forecasted_demand,
        },
        result,
    )

    return result


def get_warehouse_status(tool_context: ToolContext) -> dict:
    """
    Get current stock levels and utilisation across ALL warehouses.
    Use this for a full network-wide inventory picture without a specific product.
    """
    result = _inventory_svc.get_warehouse_status()

    state = _get_state(tool_context)
    state.update(result)

    tool_context.state["workflow_state"] = state

    _track(
        tool_context,
        "get_warehouse_status",
        {},
        result,
    )

    return result


async def negotiate_with_vendor(
    tool_context: ToolContext, product_sku: str, quantity: int, urgency: str = "normal"
) -> dict:
    """
    Source products from suppliers: send RFQs, compare quotes, negotiate price,
    and generate a confirmed purchase order.
    Call this when optimize_inventory reports reorder_needed = True.

    Args:
        product_sku: Product SKU to source
        quantity: Quantity to order (use reorder_quantity from optimize_inventory)
        urgency: normal | high  — high adds 10% premium but faster delivery
    """
    result = await _vendor_svc.negotiate_with_vendor(product_sku, quantity, urgency)

    state = _get_state(tool_context)
    state.update(result)

    tool_context.state["workflow_state"] = state
    _track(
        tool_context,
        "negotiate_with_vendor",
        {
            "product_sku": product_sku,
            "quantity": quantity,
            "urgency": urgency,
        },
        result,
    )

    return result


async def plan_delivery_route(
    tool_context: ToolContext, transfers: list[dict], urgency: str = "normal"
) -> dict:
    """
    Optimise delivery routes for inventory transfers or supplier shipments.
    Selects the best transport mode (truck / express / train) by distance & urgency.

    Args:
        transfers: List of dicts, each with keys: from_warehouse, to_warehouse,
                   quantity (int), distance_km (int)
        urgency: normal | high
    """
    result = await _routing_svc.plan_delivery_route(transfers, urgency)
    state = _get_state(tool_context)
    state.update(result)

    tool_context.state["workflow_state"] = state
    _track(
        tool_context,
        "plan_delivery_route",
        {
            "transfers": transfers,
            "urgency": urgency,
        },
        result,
    )
    return result


async def send_supply_alerts(
    tool_context: ToolContext,
    event_description: str,
    region: str,
    spike_multiplier: float,
    peak_demand: int,
    reorder_quantity: int,
    vendor_selected: str,
    total_cost: int,
    severity: str = "high",
) -> dict:
    """
    Send Slack/email notifications to stakeholders and create an audit record.
    Call this as the FINAL step after all other agents have completed their work.

    Args:
        event_description: Short description of the triggering event (e.g. "Cyclone in Mumbai")
        region: Affected region
        spike_multiplier: Demand multiplier detected (e.g. 12 for 12x spike)
        peak_demand: Peak demand units forecast
        reorder_quantity: Units ordered from external supplier (0 if none)
        vendor_selected: Name of the supplier selected (empty string if none)
        total_cost: Total procurement cost in rupees (0 if none)
        severity: info | high | critical
    """
    state = _get_state(tool_context)
    event_summary = {
        "event": {"description": event_description, "region": region},
        "demand": {
            "spike_detected": spike_multiplier > 1,
            "spike_multiplier": spike_multiplier,
            "peak_demand": peak_demand,
        },
        "inventory": {
            "reorder_needed": reorder_quantity > 0,
            "reorder_quantity": reorder_quantity,
            "transfers": state.get("transfers", []),
        },
        "vendor": {
            "vendor_selected": vendor_selected,
            "total_price": total_cost,
        },
        "routing": {
            "routes": state.get("routes", []),
            "total_cost": state.get("routing_total_cost", 0),
            "earliest_delivery": state.get("earliest_delivery"),
        },
    }
    result = await _alert_svc.send_alerts(
        event_summary=event_summary, severity=severity
    )

    state["alert_severity"] = severity

    tool_context.state["workflow_state"] = state
    _track(
        tool_context,
        "send_supply_alerts",
        {
            "event_description": event_description,
            "region": region,
            "severity": severity,
        },
        result,
    )

    return result


async def list_all_products(tool_context: ToolContext) -> dict:
    """
    List all products in the supply chain network with their SKUs, names, and categories.
    This can be used for inventory checks or vendor negotiations when product details are needed.
    """
    result = await _inventory_svc.list_products()

    state = _get_state(tool_context)
    state.update({"products": result})

    tool_context.state["workflow_state"] = state
    _track(
        tool_context,
        "list_all_products",
        {
            "products_count": len(result),
            "products": result,
        },
        result,
    )

    return result
