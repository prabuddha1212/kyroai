from typing import Optional, Dict, Any
from pydantic import BaseModel

class AnalyticsEventRequest(BaseModel):
    event_name: str
    product_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
