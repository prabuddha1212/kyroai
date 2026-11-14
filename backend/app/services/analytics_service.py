from collections import defaultdict
from typing import Dict, List, Any
from app.db.supabase_client import supabase
from app.models.analytics import AnalyticsEventRequest

_in_memory_analytics: List[Dict[str, Any]] = []

class AnalyticsService:
    @staticmethod
    def record_event(payload: AnalyticsEventRequest) -> Dict[str, str]:
        event_data = {
            "event_name": payload.event_name,
            "product_id": payload.product_id,
            "meta": payload.meta or {},
        }
        try:
            if supabase:
                supabase.table("analytics_events").insert(event_data).execute()
                return {"status": "recorded"}
        except Exception:
            pass

        _in_memory_analytics.append(event_data)
        return {"status": "recorded_locally"}

    @staticmethod
    def get_event_counts() -> Dict[str, int]:
        event_counts: Dict[str, int] = defaultdict(int)
        try:
            if supabase:
                analytics_res = supabase.table("analytics_events").select("event_name").execute()
                if analytics_res.data:
                    for row in analytics_res.data:
                        event_counts[row.get("event_name")] += 1
        except Exception:
            pass

        for ev in _in_memory_analytics:
            event_counts[ev["event_name"]] += 1

        return dict(event_counts)
