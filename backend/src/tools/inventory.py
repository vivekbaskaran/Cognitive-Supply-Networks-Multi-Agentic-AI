from datetime import datetime
from typing import Dict, Any, List
from src.data.products import INITIAL_INVENTORY, PRODUCT_CATALOG


class InventoryAgent:
    """
    Optimizes inventory allocation across warehouses:
    - Checks current stock levels
    - Identifies gaps vs demand forecast
    - Plans inter-warehouse transfers
    - Recommends external purchases
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.name = "inventory"
        
    async def optimize_inventory(
        self,
        product_sku: str,
        region: str,
        forecasted_demand: int,
        current_stock: int = None
    ) -> Dict[str, Any]:
        """
        Main entry point for inventory optimization
        
        Called by Google ADK as a tool
        """
        print(f"\nINVENTORY AGENT: Optimizing stock for {product_sku} in {region}")
        
        # 1. Get current inventory across all warehouses
        inventory_status = self._get_inventory_status(product_sku)
        
        # 2. Find the target warehouse
        target_warehouse = self._find_warehouse(region)
        if not target_warehouse:
            return {"status": "error", "message": f"Warehouse not found for {region}"}
        
        current_stock_target = inventory_status["by_warehouse"].get(
            target_warehouse["id"], 0
        )
        
        print(f"   Current stock in {region}: {current_stock_target} units")
        print(f"   Forecasted demand: {forecasted_demand} units")
        
        # 3. Calculate gap
        gap = forecasted_demand - current_stock_target
        
        if gap <= 0:
            print(f"Stock sufficient! Surplus: {abs(gap)} units")
            return {
                "status": "success",
                "action": "none_needed",
                "current_stock": current_stock_target,
                "forecasted_demand": forecasted_demand,
                "surplus": abs(gap),
                "message": "Stock levels adequate"
            }
        
        print(f"SHORTFALL: {gap} units needed!")
        
        # 4. Find surplus in other warehouses
        transfers = self._plan_transfers(
            product_sku=product_sku,
            target_warehouse_id=target_warehouse["id"],
            needed_quantity=gap,
            inventory_status=inventory_status
        )
        
        total_transferable = sum(t["quantity"] for t in transfers)
        remaining_gap = gap - total_transferable
        
        # 5. Determine if external order needed
        reorder_needed = remaining_gap > 0
        safety_buffer = int(gap * 0.2)  # 20% safety buffer
        
        result = {
            "status": "success",
            "product_sku": product_sku,
            "target_region": region,
            "target_warehouse": target_warehouse["name"],
            "current_stock": current_stock_target,
            "forecasted_demand": forecasted_demand,
            "gap": gap,
            "transfers": transfers,
            "total_transferable": total_transferable,
            "reorder_needed": reorder_needed,
            "reorder_quantity": remaining_gap + safety_buffer if reorder_needed else 0,
            "safety_buffer": safety_buffer,
            "estimated_cost_transfers": sum(t["estimated_cost"] for t in transfers),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        print(f"Solution found:")
        if transfers:
            print(f"      - Internal transfers: {total_transferable} units from {len(transfers)} warehouses")
        if reorder_needed:
            print(f"      - External order: {result['reorder_quantity']} units (includes {safety_buffer} buffer)")
        
        return result
    
    def _get_inventory_status(self, product_sku: str) -> Dict:
        """Get current inventory across all warehouses"""
        by_warehouse = {}
        total = 0
        
        for warehouse in INITIAL_INVENTORY["warehouses"]:
            stock = warehouse["stock"].get(product_sku, 0)
            by_warehouse[warehouse["id"]] = stock
            total += stock
        
        return {
            "product_sku": product_sku,
            "total_network": total,
            "by_warehouse": by_warehouse
        }
    
    def _find_warehouse(self, region: str) -> Dict:
        """Find warehouse for a region"""
        region_map = {
            "Mumbai": "WH-MUM",
            "Delhi": "WH-DEL",
            "Bangalore": "WH-BLR",
            "Chennai": "WH-CHN",
            "Kolkata": "WH-KOL"
        }
        
        warehouse_id = region_map.get(region)
        if not warehouse_id:
            return None
        
        for wh in INITIAL_INVENTORY["warehouses"]:
            if wh["id"] == warehouse_id:
                return wh
        return None
    
    def _plan_transfers(
        self,
        product_sku: str,
        target_warehouse_id: str,
        needed_quantity: int,
        inventory_status: Dict
    ) -> List[Dict]:
        """Plan inter-warehouse transfers"""
        transfers = []
        remaining_need = needed_quantity
        
        # Calculate surplus in each warehouse
        for warehouse in INITIAL_INVENTORY["warehouses"]:
            if warehouse["id"] == target_warehouse_id:
                continue  # Skip target warehouse
            
            current_stock = warehouse["stock"].get(product_sku, 0)
            
            # Keep minimum 30% in source warehouse
            min_stock = int(current_stock * 0.3)
            available_for_transfer = max(0, current_stock - min_stock)
            
            if available_for_transfer > 0 and remaining_need > 0:
                transfer_qty = min(available_for_transfer, remaining_need)
                
                # Calculate cost (mock)
                distance_map = {
                    ("WH-DEL", "WH-MUM"): 1400,
                    ("WH-BLR", "WH-MUM"): 980,
                    ("WH-CHN", "WH-MUM"): 1300,
                    ("WH-KOL", "WH-MUM"): 1900,
                }
                
                distance = distance_map.get(
                    (warehouse["id"], target_warehouse_id), 1000
                )
                cost_per_km = 10
                estimated_cost = (distance * cost_per_km) + (transfer_qty * 5)
                
                transfers.append({
                    "from_warehouse": warehouse["name"],
                    "from_warehouse_id": warehouse["id"],
                    "quantity": transfer_qty,
                    "distance_km": distance,
                    "estimated_cost": estimated_cost,
                    "transit_time_hours": int(distance / 60),  # Assume 60 km/hr
                    "mode": "truck"
                })
                
                remaining_need -= transfer_qty
        
        return transfers
    
    def get_warehouse_status(self) -> Dict:
        """Get status of all warehouses (for chat agent)"""
        warehouses = []
        
        for wh in INITIAL_INVENTORY["warehouses"]:
            total_items = sum(wh["stock"].values())
            utilization = (total_items / wh["capacity"]) * 100
            
            warehouses.append({
                "id": wh["id"],
                "name": wh["name"],
                "location": wh["location"],
                "capacity": wh["capacity"],
                "current_stock": total_items,
                "utilization_percent": round(utilization, 1),
                "status": "healthy" if utilization < 80 else "near_capacity"
            })
        
        return {"warehouses": warehouses}
    
    async def list_products(self) -> List[Dict]:
        """List all products (for chat agent)"""
        all_products = []

        for category in PRODUCT_CATALOG["categories"]:
            all_products.extend(category["products"])

        return all_products


# ADK Tool Definition
INVENTORY_AGENT_TOOL = {
    "name": "optimize_inventory",
    "description": """
    Optimize inventory allocation across warehouses.
    Checks current stock, identifies gaps, plans transfers between warehouses,
    and recommends external purchases if needed.
    Use this after getting demand forecast to ensure adequate stock.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "product_sku": {
                "type": "string",
                "description": "Product SKU to optimize"
            },
            "region": {
                "type": "string",
                "description": "Target region (Mumbai, Delhi, Bangalore, Chennai, Kolkata)"
            },
            "forecasted_demand": {
                "type": "integer",
                "description": "Predicted demand quantity (from demand agent)"
            },
            "current_stock": {
                "type": "integer",
                "description": "Current stock in target warehouse (optional)"
            }
        },
        "required": ["product_sku", "region", "forecasted_demand"]
    }
}


# Test function
async def test_inventory_agent():
    """Test the inventory agent"""
    agent = InventoryAgent(demo_mode=True)
    
    # Simulate demand forecast of 348 units for Mumbai
    result = await agent.optimize_inventory(
        product_sku="RC-FULL-NVY-M",
        region="Mumbai",
        forecasted_demand=348
    )
    
    print("\nOPTIMIZATION RESULT:")
    print(f"   Gap: {result['gap']} units")
    print(f"   Transfers planned: {len(result['transfers'])}")
    print(f"   External order needed: {result['reorder_needed']}")
    if result['reorder_needed']:
        print(f"   Order quantity: {result['reorder_quantity']} units")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_inventory_agent())
