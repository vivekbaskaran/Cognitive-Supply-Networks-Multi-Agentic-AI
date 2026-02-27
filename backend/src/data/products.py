"""
data/products.py
Fashion product catalog for StyleFlow India
"""

PRODUCT_CATALOG = {
    "categories": [
        {
            "id": "winter_wear",
            "name": "Winter Wear",
            "products": [
                {
                    "sku": "WJ-DNM-BLK-M",
                    "name": "Denim Winter Jacket - Black - Medium",
                    "category": "Winter Jackets",
                    "base_sku": "WJ-DNM",
                    "color": "Black",
                    "size": "M",
                    "price": 2499,
                    "cost": 800,
                    "margin_percent": 68,
                    "suppliers": ["Fashion Hub Delhi", "Winter Wear Co"],
                    "demand_pattern": "seasonal_winter",
                    "avg_daily_sales": 12,
                    "spike_triggers": ["temperature_drop", "winter_start", "festival_diwali"]
                },
                {
                    "sku": "WJ-DNM-BLK-L",
                    "name": "Denim Winter Jacket - Black - Large",
                    "category": "Winter Jackets",
                    "base_sku": "WJ-DNM",
                    "color": "Black",
                    "size": "L",
                    "price": 2499,
                    "cost": 800,
                    "margin_percent": 68,
                    "suppliers": ["Fashion Hub Delhi", "Winter Wear Co"],
                    "demand_pattern": "seasonal_winter",
                    "avg_daily_sales": 18,
                    "spike_triggers": ["temperature_drop", "winter_start", "festival_diwali"]
                },
                {
                    "sku": "WJ-DNM-BLK-XL",
                    "name": "Denim Winter Jacket - Black - XL",
                    "category": "Winter Jackets",
                    "base_sku": "WJ-DNM",
                    "color": "Black",
                    "size": "XL",
                    "price": 2499,
                    "cost": 800,
                    "margin_percent": 68,
                    "suppliers": ["Fashion Hub Delhi", "Winter Wear Co"],
                    "demand_pattern": "seasonal_winter",
                    "avg_daily_sales": 15,
                    "spike_triggers": ["temperature_drop", "winter_start", "festival_diwali"]
                },
                {
                    "sku": "SW-HOOD-GRY-L",
                    "name": "Hooded Sweatshirt - Grey - Large",
                    "category": "Sweatshirts",
                    "base_sku": "SW-HOOD",
                    "color": "Grey",
                    "size": "L",
                    "price": 1299,
                    "cost": 420,
                    "margin_percent": 68,
                    "suppliers": ["Cotton Comfort Ltd"],
                    "demand_pattern": "seasonal_winter",
                    "avg_daily_sales": 25,
                    "spike_triggers": ["temperature_drop", "winter_start"]
                }
            ]
        },
        {
            "id": "monsoon_wear",
            "name": "Monsoon Essentials",
            "products": [
                {
                    "sku": "RC-FULL-NVY-M",
                    "name": "Full-Length Raincoat - Navy Blue - Medium",
                    "category": "Raincoats",
                    "base_sku": "RC-FULL",
                    "color": "Navy Blue",
                    "size": "M",
                    "price": 899,
                    "cost": 280,
                    "margin_percent": 69,
                    "suppliers": ["RainShield Fashion", "Monsoon Styles"],
                    "demand_pattern": "weather_monsoon",
                    "avg_daily_sales": 8,
                    "spike_triggers": ["heavy_rain_forecast", "cyclone_warning", "monsoon_start"],
                    "spike_multiplier": 12.0  # 12x spike during heavy rain!
                },
                {
                    "sku": "RC-FULL-NVY-L",
                    "name": "Full-Length Raincoat - Navy Blue - Large",
                    "category": "Raincoats",
                    "base_sku": "RC-FULL",
                    "color": "Navy Blue",
                    "size": "L",
                    "price": 899,
                    "cost": 280,
                    "margin_percent": 69,
                    "suppliers": ["RainShield Fashion", "Monsoon Styles"],
                    "demand_pattern": "weather_monsoon",
                    "avg_daily_sales": 12,
                    "spike_triggers": ["heavy_rain_forecast", "cyclone_warning", "monsoon_start"],
                    "spike_multiplier": 12.0
                },
                {
                    "sku": "WP-SHOE-BLK-42",
                    "name": "Waterproof Sneakers - Black - Size 42",
                    "category": "Footwear",
                    "base_sku": "WP-SHOE",
                    "color": "Black",
                    "size": "42",
                    "price": 1799,
                    "cost": 580,
                    "margin_percent": 68,
                    "suppliers": ["FootWear Direct"],
                    "demand_pattern": "weather_monsoon",
                    "avg_daily_sales": 15,
                    "spike_triggers": ["heavy_rain_forecast", "monsoon_start"],
                    "spike_multiplier": 5.0
                }
            ]
        },
        {
            "id": "summer_wear",
            "name": "Summer Collection",
            "products": [
                {
                    "sku": "TS-CREW-WHT-M",
                    "name": "Crew Neck T-Shirt - White - Medium",
                    "category": "T-Shirts",
                    "base_sku": "TS-CREW",
                    "color": "White",
                    "size": "M",
                    "price": 499,
                    "cost": 150,
                    "margin_percent": 70,
                    "suppliers": ["Cotton Mills India", "Textile Hub"],
                    "demand_pattern": "seasonal_summer",
                    "avg_daily_sales": 45,
                    "spike_triggers": ["temperature_rise", "summer_sale"]
                },
                {
                    "sku": "TS-CREW-WHT-L",
                    "name": "Crew Neck T-Shirt - White - Large",
                    "category": "T-Shirts",
                    "base_sku": "TS-CREW",
                    "color": "White",
                    "size": "L",
                    "price": 499,
                    "cost": 150,
                    "margin_percent": 70,
                    "suppliers": ["Cotton Mills India", "Textile Hub"],
                    "demand_pattern": "seasonal_summer",
                    "avg_daily_sales": 52,
                    "spike_triggers": ["temperature_rise", "summer_sale"]
                }
            ]
        },
        {
            "id": "festival_wear",
            "name": "Festival Special",
            "products": [
                {
                    "sku": "KT-SILK-RED-M",
                    "name": "Silk Kurta - Red - Medium",
                    "category": "Ethnic Wear",
                    "base_sku": "KT-SILK",
                    "color": "Red",
                    "size": "M",
                    "price": 1899,
                    "cost": 620,
                    "margin_percent": 67,
                    "suppliers": ["Ethnic Fashion House"],
                    "demand_pattern": "festival_driven",
                    "avg_daily_sales": 8,
                    "spike_triggers": ["diwali", "navratri", "wedding_season"],
                    "spike_multiplier": 8.0
                }
            ]
        }
    ]
}


# Initial inventory across 5 warehouses
INITIAL_INVENTORY = {
    "warehouses": [
        {
            "id": "WH-MUM",
            "name": "Mumbai Warehouse",
            "location": "Andheri East, Mumbai",
            "capacity": 50000,
            "stock": {
                "WJ-DNM-BLK-M": 120,
                "WJ-DNM-BLK-L": 180,
                "WJ-DNM-BLK-XL": 150,
                "SW-HOOD-GRY-L": 280,
                "RC-FULL-NVY-M": 50,   # LOW! Will cause alert
                "RC-FULL-NVY-L": 80,
                "WP-SHOE-BLK-42": 120,
                "TS-CREW-WHT-M": 450,
                "TS-CREW-WHT-L": 520,
                "KT-SILK-RED-M": 60
            }
        },
        {
            "id": "WH-DEL",
            "name": "Delhi Warehouse",
            "location": "Naraina, Delhi",
            "capacity": 40000,
            "stock": {
                "WJ-DNM-BLK-M": 200,
                "WJ-DNM-BLK-L": 280,
                "WJ-DNM-BLK-XL": 220,
                "SW-HOOD-GRY-L": 350,
                "RC-FULL-NVY-M": 180,  # SURPLUS! Can transfer
                "RC-FULL-NVY-L": 220,  # SURPLUS!
                "WP-SHOE-BLK-42": 180,
                "TS-CREW-WHT-M": 380,
                "TS-CREW-WHT-L": 420,
                "KT-SILK-RED-M": 80
            }
        },
        {
            "id": "WH-BLR",
            "name": "Bangalore Warehouse",
            "location": "Whitefield, Bangalore",
            "capacity": 35000,
            "stock": {
                "WJ-DNM-BLK-M": 100,
                "WJ-DNM-BLK-L": 150,
                "WJ-DNM-BLK-XL": 120,
                "SW-HOOD-GRY-L": 200,
                "RC-FULL-NVY-M": 120,  # SURPLUS!
                "RC-FULL-NVY-L": 160,
                "WP-SHOE-BLK-42": 150,
                "TS-CREW-WHT-M": 500,
                "TS-CREW-WHT-L": 580,
                "KT-SILK-RED-M": 40
            }
        },
        {
            "id": "WH-CHN",
            "name": "Chennai Warehouse",
            "location": "Ambattur, Chennai",
            "capacity": 25000,
            "stock": {
                "WJ-DNM-BLK-M": 60,
                "WJ-DNM-BLK-L": 80,
                "WJ-DNM-BLK-XL": 70,
                "SW-HOOD-GRY-L": 120,
                "RC-FULL-NVY-M": 40,
                "RC-FULL-NVY-L": 60,
                "WP-SHOE-BLK-42": 80,
                "TS-CREW-WHT-M": 350,
                "TS-CREW-WHT-L": 420,
                "KT-SILK-RED-M": 30
            }
        },
        {
            "id": "WH-KOL",
            "name": "Kolkata Warehouse",
            "location": "Salt Lake, Kolkata",
            "capacity": 30000,
            "stock": {
                "WJ-DNM-BLK-M": 90,
                "WJ-DNM-BLK-L": 120,
                "WJ-DNM-BLK-XL": 100,
                "SW-HOOD-GRY-L": 180,
                "RC-FULL-NVY-M": 70,
                "RC-FULL-NVY-L": 100,
                "WP-SHOE-BLK-42": 100,
                "TS-CREW-WHT-M": 280,
                "TS-CREW-WHT-L": 320,
                "KT-SILK-RED-M": 50
            }
        }
    ]
}


# Supplier database
SUPPLIERS = {
    "suppliers": [
        {
            "id": "SUP-001",
            "name": "Fashion Hub Delhi",
            "location": "Noida, Delhi NCR",
            "rating": 96,
            "min_order_quantity": 100,
            "avg_delivery_days": 3,
            "specialties": ["Winter Wear", "Jackets"],
            "payment_terms": "Net 30",
            "contact": "procurement@fashionhub.in"
        },
        {
            "id": "SUP-002",
            "name": "RainShield Fashion",
            "location": "Pune, Maharashtra",
            "rating": 94,
            "min_order_quantity": 50,
            "avg_delivery_days": 2,
            "specialties": ["Rainwear", "Monsoon Essentials"],
            "payment_terms": "Net 30",
            "contact": "sales@rainshield.in"
        },
        {
            "id": "SUP-003",
            "name": "Cotton Mills India",
            "location": "Coimbatore, Tamil Nadu",
            "rating": 98,
            "min_order_quantity": 200,
            "avg_delivery_days": 4,
            "specialties": ["T-Shirts", "Cotton Wear"],
            "payment_terms": "Net 45",
            "contact": "orders@cottonmills.in"
        },
        {
            "id": "SUP-004",
            "name": "Winter Wear Co",
            "location": "Ludhiana, Punjab",
            "rating": 92,
            "min_order_quantity": 80,
            "avg_delivery_days": 3,
            "specialties": ["Sweatshirts", "Hoodies", "Winter Jackets"],
            "payment_terms": "Net 30",
            "contact": "business@winterwear.in"
        },
        {
            "id": "SUP-005",
            "name": "Monsoon Styles",
            "location": "Mumbai, Maharashtra",
            "rating": 90,
            "min_order_quantity": 50,
            "avg_delivery_days": 1,  # Local supplier!
            "specialties": ["Raincoats", "Waterproof Accessories"],
            "payment_terms": "Net 15",
            "contact": "quick@monsoonstyles.in"
        },
        {
            "id": "SUP-006",
            "name": "Ethnic Fashion House",
            "location": "Surat, Gujarat",
            "rating": 95,
            "min_order_quantity": 50,
            "avg_delivery_days": 3,
            "specialties": ["Ethnic Wear", "Festival Collection"],
            "payment_terms": "Net 30",
            "contact": "info@ethnicfashion.in"
        }
    ]
}


# Demo events that trigger demand spikes
DEMO_EVENTS = {
    "monsoon_cyclone": {
        "name": "Cyclone Nisarga Approaching Mumbai",
        "date": "2024-06-12",
        "affected_regions": ["Mumbai", "Pune"],
        "affected_products": ["RC-FULL-NVY-M", "RC-FULL-NVY-L", "WP-SHOE-BLK-42"],
        "spike_multiplier": 12.0,
        "duration_days": 3
    },
    "winter_cold_wave": {
        "name": "Cold Wave Hits North India",
        "date": "2024-12-15",
        "affected_regions": ["Delhi", "Chandigarh", "Jaipur"],
        "affected_products": ["WJ-DNM-BLK-M", "WJ-DNM-BLK-L", "SW-HOOD-GRY-L"],
        "spike_multiplier": 6.0,
        "duration_days": 7
    },
    "festival_diwali": {
        "name": "Diwali Festival Sale",
        "date": "2024-10-20",
        "affected_regions": ["All"],
        "affected_products": ["KT-SILK-RED-M"],
        "spike_multiplier": 8.0,
        "duration_days": 10
    }
}
