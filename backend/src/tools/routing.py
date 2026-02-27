from datetime import datetime, timedelta
from typing import Dict, Any, List


class RoutingAgent:
    """
    Optimizes delivery routes:
    - Plans fastest/cheapest routes
    - Considers traffic, weather
    - Selects transport mode
    - Estimates delivery times
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.name = "routing"
    
    async def plan_delivery_route(
        self,
        transfers: List[Dict],
        urgency: str = "normal"
    ) -> Dict[str, Any]:
        """
        Main entry point for route planning
        
        Called by Google ADK as a tool
        """
        print(f"\nROUTING AGENT: Planning delivery for {len(transfers)} shipments")
        
        optimized_routes = []
        total_cost = 0
        earliest_eta = None
        
        for transfer in transfers:
            route = await self._optimize_single_route(
                from_location=transfer.get("from_warehouse", transfer.get("source")),
                to_location=transfer.get("to_warehouse", transfer.get("destination", "Mumbai")),
                quantity=transfer["quantity"],
                distance_km=transfer.get("distance_km", 1000),
                urgency=urgency
            )
            
            optimized_routes.append(route)
            total_cost += route["cost"]
            
            # Track earliest delivery
            if not earliest_eta or route["eta_datetime"] < earliest_eta:
                earliest_eta = route["eta_datetime"]
            
            print(f"{route['from']} → {route['to']}: {route['mode']} ({route['eta_hours']}h, ₹{route['cost']:,})")
        
        return {
            "status": "success",
            "routes": optimized_routes,
            "total_routes": len(optimized_routes),
            "total_cost": total_cost,
            "earliest_delivery": earliest_eta,
            "average_delivery_hours": sum(r["eta_hours"] for r in optimized_routes) / len(optimized_routes),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _optimize_single_route(
        self,
        from_location: str,
        to_location: str,
        quantity: int,
        distance_km: int,
        urgency: str
    ) -> Dict:
        """Optimize a single delivery route"""
        
        # Determine best transport mode
        if urgency == "high" and distance_km < 500:
            mode = "express_truck"
            speed_kmh = 60
            cost_per_km = 15
        elif distance_km > 1500:
            mode = "train"
            speed_kmh = 50
            cost_per_km = 8
        else:
            mode = "truck"
            speed_kmh = 55
            cost_per_km = 10
        
        # Calculate timing
        transit_hours = int(distance_km / speed_kmh)
        base_cost = distance_km * cost_per_km
        handling_cost = quantity * 2  # ₹2 per unit
        total_cost = base_cost + handling_cost
        
        eta_datetime = datetime.now() + timedelta(hours=transit_hours)
        
        # Weather check (mock)
        weather_delay = 0
        if self.demo_mode:
            # Simulate weather impact
            if "Mumbai" in to_location and datetime.now().day % 2 == 0:
                weather_delay = 2
                transit_hours += weather_delay
        
        return {
            "from": from_location,
            "to": to_location,
            "distance_km": distance_km,
            "mode": mode,
            "quantity": quantity,
            "eta_hours": transit_hours,
            "eta_datetime": eta_datetime.isoformat(),
            "eta_display": eta_datetime.strftime("%Y-%m-%d %H:%M"),
            "cost": total_cost,
            "weather_delay_hours": weather_delay,
            "carrier": self._select_carrier(mode),
            "tracking_available": True
        }
    
    def _select_carrier(self, mode: str) -> str:
        """Select logistics carrier based on mode"""
        carriers = {
            "express_truck": "BlueDart Express",
            "truck": "DTDC Logistics",
            "train": "Indian Railways Cargo"
        }
        return carriers.get(mode, "Standard Logistics")


# ADK Tool Definition
ROUTING_AGENT_TOOL = {
    "name": "plan_delivery_route",
    "description": """
    Optimize delivery routes for inventory transfers or supplier shipments.
    Considers distance, traffic, weather, and selects best transport mode.
    Returns route details with ETA and costs.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "transfers": {
                "type": "array",
                "description": "List of transfers to route",
                "items": {
                    "type": "object",
                    "properties": {
                        "from_warehouse": {"type": "string"},
                        "to_warehouse": {"type": "string"},
                        "quantity": {"type": "integer"},
                        "distance_km": {"type": "integer"}
                    }
                }
            },
            "urgency": {
                "type": "string",
                "description": "Urgency: normal or high",
                "enum": ["normal", "high"]
            }
        },
        "required": ["transfers"]
    }
}


# Test
async def test_routing_agent():
    agent = RoutingAgent(demo_mode=True)
    result = await agent.plan_delivery_route(
        transfers=[
            {"from_warehouse": "Delhi", "to_warehouse": "Mumbai", "quantity": 180, "distance_km": 1400},
            {"from_warehouse": "Bangalore", "to_warehouse": "Mumbai", "quantity": 120, "distance_km": 980}
        ],
        urgency="high"
    )
    print(f"\nPlanned {result['total_routes']} routes, total cost: ₹{result['total_cost']:,}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_routing_agent())
