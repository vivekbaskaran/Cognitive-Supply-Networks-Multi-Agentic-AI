from datetime import datetime, timedelta
from typing import Dict, Any, List
from src.data.products import SUPPLIERS


class VendorAgent:
    """
    Manages vendor relationships and procurement:
    - Sends RFQs to suppliers
    - Compares quotes
    - Negotiates prices
    - Generates purchase orders
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.name = "vendor"
    
    async def negotiate_with_vendor(
        self,
        product_sku: str,
        quantity: int,
        urgency: str = "normal",
        budget_limit: int = None
    ) -> Dict[str, Any]:
        """
        Main entry point for vendor negotiation
        
        Called by Google ADK as a tool
        """
        print(f"\n💼 VENDOR AGENT: Sourcing {quantity} units of {product_sku}")
        
        # 1. Find eligible suppliers
        eligible_suppliers = self._find_suppliers(product_sku)
        
        if not eligible_suppliers:
            return {
                "status": "error",
                "message": f"No suppliers found for {product_sku}"
            }
        
        print(f"   Found {len(eligible_suppliers)} eligible suppliers")
        
        # 2. Send RFQs and get quotes
        quotes = await self._get_quotes(
            product_sku=product_sku,
            quantity=quantity,
            suppliers=eligible_suppliers,
            urgency=urgency
        )
        
        print(f"   Received {len(quotes)} quotes")
        
        # 3. Evaluate and select best vendor
        best_quote = self._select_best_vendor(
            quotes=quotes,
            quantity=quantity,
            urgency=urgency,
            budget_limit=budget_limit
        )
        
        if not best_quote:
            return {
                "status": "error",
                "message": "No suitable vendor found within constraints"
            }
        
        # 4. Attempt negotiation
        final_quote = await self._negotiate(best_quote, quantity)
        
        # 5. Generate PO
        purchase_order = self._generate_po(
            quote=final_quote,
            product_sku=product_sku,
            quantity=quantity
        )
        
        print(f"Selected: {final_quote['supplier_name']}")
        print(f"Price: ₹{final_quote['unit_price']}/unit")
        print(f"Total: ₹{final_quote['total_price']:,}")
        print(f"Delivery: {final_quote['delivery_days']} days")
        
        return {
            "status": "success",
            "product_sku": product_sku,
            "quantity": quantity,
            "vendor_selected": final_quote["supplier_name"],
            "vendor_id": final_quote["supplier_id"],
            "unit_price": final_quote["unit_price"],
            "total_price": final_quote["total_price"],
            "delivery_days": final_quote["delivery_days"],
            "delivery_date": final_quote["delivery_date"],
            "purchase_order": purchase_order,
            "po_confirmed": True,
            "quotes_compared": len(quotes),
            "negotiation_savings": final_quote.get("savings", 0),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _find_suppliers(self, product_sku: str) -> List[Dict]:
        """Find suppliers that can provide the product"""
        # Determine product type
        product_type = None
        if "RC-" in product_sku or "WP-" in product_sku:
            product_type = "Rainwear"
        elif "WJ-" in product_sku or "SW-" in product_sku:
            product_type = "Winter Wear"
        elif "TS-" in product_sku:
            product_type = "T-Shirts"
        elif "KT-" in product_sku:
            product_type = "Ethnic Wear"
        
        eligible = []
        for supplier in SUPPLIERS["suppliers"]:
            # Check if supplier specializes in this category
            for specialty in supplier["specialties"]:
                if product_type and product_type.lower() in specialty.lower():
                    eligible.append(supplier)
                    break
        
        return eligible
    
    async def _get_quotes(
        self,
        product_sku: str,
        quantity: int,
        suppliers: List[Dict],
        urgency: str
    ) -> List[Dict]:
        """Get quotes from suppliers (mock in demo)"""
        quotes = []
        
        base_prices = {
            "RC-FULL-NVY-M": 280,
            "RC-FULL-NVY-L": 280,
            "WP-SHOE-BLK-42": 580,
            "WJ-DNM-BLK-M": 800,
            "WJ-DNM-BLK-L": 800,
            "SW-HOOD-GRY-L": 420,
            "TS-CREW-WHT-M": 150,
            "KT-SILK-RED-M": 620
        }
        
        base_price = base_prices.get(product_sku, 300)
        
        for supplier in suppliers:
            # Vary price based on supplier rating
            price_factor = 1.0 + ((100 - supplier["rating"]) / 200)
            unit_price = int(base_price * price_factor)
            
            # Urgency premium
            if urgency == "high":
                unit_price = int(unit_price * 1.1)
                delivery_days = supplier["avg_delivery_days"] - 1
            else:
                delivery_days = supplier["avg_delivery_days"]
            
            # Check MOQ
            if quantity < supplier["min_order_quantity"]:
                continue
            
            quotes.append({
                "supplier_id": supplier["id"],
                "supplier_name": supplier["name"],
                "supplier_rating": supplier["rating"],
                "unit_price": unit_price,
                "total_price": unit_price * quantity,
                "delivery_days": delivery_days,
                "delivery_date": (datetime.now() + timedelta(days=delivery_days)).strftime("%Y-%m-%d"),
                "payment_terms": supplier["payment_terms"],
                "location": supplier["location"]
            })
        
        return quotes
    
    def _select_best_vendor(
        self,
        quotes: List[Dict],
        quantity: int,
        urgency: str,
        budget_limit: int
    ) -> Dict:
        """Select best vendor based on criteria"""
        if not quotes:
            return None
        
        # Filter by budget
        if budget_limit:
            quotes = [q for q in quotes if q["total_price"] <= budget_limit]
        
        if not quotes:
            return None
        
        # Score each quote
        for quote in quotes:
            score = 0
            
            # Price score (lower is better)
            min_price = min(q["total_price"] for q in quotes)
            price_score = (min_price / quote["total_price"]) * 40
            score += price_score
            
            # Quality score
            quality_score = (quote["supplier_rating"] / 100) * 30
            score += quality_score
            
            # Delivery score (faster is better)
            min_delivery = min(q["delivery_days"] for q in quotes)
            delivery_score = (min_delivery / quote["delivery_days"]) * 30
            score += delivery_score
            
            quote["score"] = score
        
        # Return highest scored
        return max(quotes, key=lambda x: x["score"])
    
    async def _negotiate(self, quote: Dict, quantity: int) -> Dict:
        """Attempt price negotiation (mock)"""
        # Simulate negotiation - get 3-5% discount for bulk
        if quantity > 200:
            discount_percent = 5
        elif quantity > 100:
            discount_percent = 3
        else:
            discount_percent = 0
        
        if discount_percent > 0:
            original_price = quote["unit_price"]
            new_price = int(original_price * (1 - discount_percent/100))
            savings = (original_price - new_price) * quantity
            
            quote["unit_price"] = new_price
            quote["total_price"] = new_price * quantity
            quote["savings"] = savings
            quote["negotiated"] = True
        else:
            quote["savings"] = 0
            quote["negotiated"] = False
        
        return quote
    
    def _generate_po(self, quote: Dict, product_sku: str, quantity: int) -> Dict:
        """Generate purchase order"""
        po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{product_sku[:6]}"
        
        return {
            "po_number": po_number,
            "supplier_id": quote["supplier_id"],
            "supplier_name": quote["supplier_name"],
            "product_sku": product_sku,
            "quantity": quantity,
            "unit_price": quote["unit_price"],
            "total_price": quote["total_price"],
            "delivery_date": quote["delivery_date"],
            "payment_terms": quote["payment_terms"],
            "issued_at": datetime.utcnow().isoformat(),
            "status": "confirmed"
        }


# ADK Tool Definition
VENDOR_AGENT_TOOL = {
    "name": "negotiate_with_vendor",
    "description": """
    Source products from suppliers by sending RFQs, comparing quotes, and negotiating prices.
    Returns purchase order details with selected vendor.
    Use this when external inventory is needed.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "product_sku": {
                "type": "string",
                "description": "Product SKU to source"
            },
            "quantity": {
                "type": "integer",
                "description": "Quantity needed"
            },
            "urgency": {
                "type": "string",
                "description": "Urgency level: normal or high",
                "enum": ["normal", "high"]
            },
            "budget_limit": {
                "type": "integer",
                "description": "Maximum budget in rupees (optional)"
            }
        },
        "required": ["product_sku", "quantity"]
    }
}


# Test
async def test_vendor_agent():
    agent = VendorAgent(demo_mode=True)
    result = await agent.negotiate_with_vendor(
        product_sku="RC-FULL-NVY-M",
        quantity=250,
        urgency="high"
    )
    print(f"\nPO Generated: {result['purchase_order']['po_number']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_vendor_agent())
