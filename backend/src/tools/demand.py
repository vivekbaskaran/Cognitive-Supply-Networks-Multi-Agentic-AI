from datetime import datetime, timedelta
from typing import Dict, Any
from src.data.products import PRODUCT_CATALOG


class DemandAgent:
    """
    Forecasts product demand based on:
    - Historical sales data
    - Weather forecasts
    - Social media trends
    - Seasonal patterns
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.name = "demand"
    
    async def forecast_demand(
        self,
        product_sku: str,
        region: str,
        event_type: str = None
    ) -> Dict[str, Any]:
        """
        Main entry point for demand forecasting
        
        This function is called by Google ADK as a tool
        """
        print(f"\nDEMAND AGENT: Analyzing demand for {product_sku} in {region}")
        
        # 1. Get product details
        product = self._get_product(product_sku)
        if not product:
            return {
                "status": "error",
                "message": f"Product {product_sku} not found"
            }
        
        # 2. Get historical sales data
        historical_data = self._get_historical_sales(product_sku, region)
        
        # 3. Check weather (mock in demo mode)
        weather_signal = await self._check_weather(region, event_type)
        
        # 4. Check social trends (mock in demo mode)  
        social_signal = self._check_social_trends(product_sku)
        
        # 5. Calculate forecast
        forecast = self._calculate_forecast(
            product=product,
            historical=historical_data,
            weather=weather_signal,
            social=social_signal,
            event_type=event_type
        )
        
        # 6. Detect spikes
        spike_detected = forecast["peak_demand"] > (historical_data["avg_daily"] * 3)
        
        print(f"Baseline demand: {historical_data['avg_daily']} units/day")
        print(f"Predicted peak: {forecast['peak_demand']} units/day")
        
        if spike_detected:
            print(f"SPIKE DETECTED: {forecast['spike_multiplier']}x normal demand!")
        
        return {
            "status": "success",
            "product_sku": product_sku,
            "product_name": product["name"],
            "region": region,
            "baseline_demand": historical_data["avg_daily"],
            "forecast": forecast["daily_forecast"],
            "peak_demand": forecast["peak_demand"],
            "peak_date": forecast["peak_date"],
            "spike_detected": spike_detected,
            "spike_multiplier": forecast["spike_multiplier"],
            "confidence": forecast["confidence"],
            "total_7day_demand": forecast["total_demand"],
            "factors": forecast["factors"],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_product(self, sku: str) -> Dict:
        """Find product in catalog"""
        for category in PRODUCT_CATALOG["categories"]:
            for product in category["products"]:
                if product["sku"] == sku:
                    return product
        return None
    
    def _get_historical_sales(self, sku: str, region: str) -> Dict:
        """Get historical sales data (mock for demo)"""
        product = self._get_product(sku)
        avg_daily = product["avg_daily_sales"] if product else 10
        
        return {
            "avg_daily": avg_daily,
            "last_30_days": avg_daily * 30,
            "trend": "stable"
        }
    
    async def _check_weather(self, region: str, event_type: str) -> Dict:
        """Check weather forecast (mock in demo mode)"""
        if self.demo_mode:
            if event_type == "cyclone" or event_type == "monsoon":
                return {
                    "condition": "heavy_rain",
                    "probability": 90,
                    "impact": "high",
                    "days_ahead": 2
                }
            elif event_type == "cold_wave":
                return {
                    "condition": "cold_wave",
                    "temperature_drop": 15,
                    "impact": "high",
                    "days_ahead": 3
                }
        
        return {
            "condition": "normal",
            "probability": 0,
            "impact": "none"
        }
    
    def _check_social_trends(self, sku: str) -> Dict:
        """Check social media trends (mock for demo)"""
        if self.demo_mode:
            return {
                "mentions": 1500,
                "sentiment": "positive",
                "trending": False
            }
        
        return {
            "mentions": 0,
            "sentiment": "neutral",
            "trending": False
        }
    
    def _calculate_forecast(
        self,
        product: Dict,
        historical: Dict,
        weather: Dict,
        social: Dict,
        event_type: str
    ) -> Dict:
        """Calculate demand forecast"""
        
        baseline = historical["avg_daily"]
        
        # Calculate multiplier based on signals
        multiplier = 1.0
        factors = []
        
        # Weather impact
        if weather["condition"] == "heavy_rain":
            if "RC-FULL" in product["sku"] or "WP-SHOE" in product["sku"]:
                multiplier *= product.get("spike_multiplier", 12.0)
                factors.append(f"Heavy rain forecast (+{multiplier}x)")
        
        elif weather["condition"] == "cold_wave":
            if "WJ-" in product["sku"] or "SW-" in product["sku"]:
                multiplier *= product.get("spike_multiplier", 6.0)
                factors.append(f"Cold wave (+{multiplier}x)")
        
        # Social signal
        if social["mentions"] > 1000 and social["trending"]:
            multiplier *= 1.2
            factors.append("Social media trending (+20%)")
        
        # Generate 7-day forecast
        peak_day = 2  # Day when demand peaks
        daily_forecast = []
        
        for day in range(7):
            if day < peak_day:
                # Building up
                daily_demand = int(baseline * (1 + (multiplier - 1) * (day / peak_day)))
            elif day == peak_day:
                # Peak day
                daily_demand = int(baseline * multiplier)
            else:
                # Declining
                days_after_peak = day - peak_day
                decline_factor = max(0.3, 1 - (days_after_peak * 0.2))
                daily_demand = int(baseline * multiplier * decline_factor)
            
            daily_forecast.append({
                "day": day + 1,
                "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                "predicted_demand": daily_demand
            })
        
        peak_demand = daily_forecast[peak_day]["predicted_demand"]
        total_demand = sum(d["predicted_demand"] for d in daily_forecast)
        
        # Confidence score
        confidence = 0.85
        if weather["impact"] == "high":
            confidence = 0.92
        
        return {
            "daily_forecast": daily_forecast,
            "peak_demand": peak_demand,
            "peak_date": daily_forecast[peak_day]["date"],
            "total_demand": total_demand,
            "spike_multiplier": round(multiplier, 1),
            "confidence": confidence,
            "factors": factors
        }


# ADK Tool Definition (for Google Gemini)
DEMAND_AGENT_TOOL = {
    "name": "forecast_demand",
    "description": """
    Forecast product demand for the next 7 days based on weather, trends, and historical data.
    Use this when you need to predict how many units of a product will be needed.
    Returns detailed forecast with spike detection.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "product_sku": {
                "type": "string",
                "description": "Product SKU (e.g., RC-FULL-NVY-M for raincoat)"
            },
            "region": {
                "type": "string",
                "description": "Region name (e.g., Mumbai, Delhi)"
            },
            "event_type": {
                "type": "string",
                "description": "Type of event: cyclone, cold_wave, festival, or null",
                "enum": ["cyclone", "cold_wave", "festival", "monsoon", None]
            }
        },
        "required": ["product_sku", "region"]
    }
}


# Test function
async def test_demand_agent():
    """Test the demand agent"""
    agent = DemandAgent(demo_mode=True)
    
    result = await agent.forecast_demand(
        product_sku="RC-FULL-NVY-M",
        region="Mumbai",
        event_type="cyclone"
    )
    
    print("\nFORECAST RESULT:")
    print(f"   Product: {result['product_name']}")
    print(f"   Baseline: {result['baseline_demand']} units/day")
    print(f"   Peak: {result['peak_demand']} units/day")
    print(f"   7-day total: {result['total_7day_demand']} units")
    print(f"   Spike: {'YES' if result['spike_detected'] else 'NO'}")
    print(f"   Confidence: {result['confidence']*100:.0f}%")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_demand_agent())
