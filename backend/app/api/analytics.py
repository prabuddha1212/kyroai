from fastapi import APIRouter
from app.models.analytics import AnalyticsEventRequest
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["analytics"])

@router.post("/analytics/event")
async def record_analytics_event(payload: AnalyticsEventRequest):
    """
    Records an analytics event (page views, button clicks, conversions).
    """
    return AnalyticsService.record_event(payload)
