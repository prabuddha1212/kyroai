from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from app.config import settings
from app.services.waitlist_service import WaitlistService
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["owner"])

@router.get("/owner/stats")
async def get_owner_stats(x_admin_key: Optional[str] = Header(None)):
    """
    Owner dashboard stats endpoint.
    Protected by secret key in X-Admin-Key header.
    """
    if not x_admin_key or x_admin_key != settings.ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin Key")

    waitlist_data = WaitlistService.get_owner_stats()
    event_counts = AnalyticsService.get_event_counts()

    return {
        "total_signups": waitlist_data["total_signups"],
        "signups_by_product": waitlist_data["signups_by_product"],
        "analytics_events": event_counts,
        "recent_signups": waitlist_data["recent_signups"],
    }
