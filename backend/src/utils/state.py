from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class SupplyChainState(BaseModel):
    product_sku: Optional[str] = None
    region: Optional[str] = None
    event_type: Optional[str] = None

    spike_detected: Optional[bool] = None
    peak_demand: Optional[int] = None
    total_7day_demand: Optional[int] = None
    confidence: Optional[float] = None

    stock_levels: Optional[Dict[str, int]] = None
    gap_size: Optional[int] = None
    reorder_needed: Optional[bool] = None

    po_number: Optional[str] = None
    vendor_name: Optional[str] = None
    delivery_date: Optional[str] = None

    transfers: Optional[List[dict]] = None
    routes: Optional[List[dict]] = None

    alert_severity: Optional[str] = None

    execution_trace: List[dict] = Field(default_factory=list)