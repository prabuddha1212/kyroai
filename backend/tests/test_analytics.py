import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_analytics_event_logging(async_client: AsyncClient):
    """Ensure analytics events are captured."""
    res = await async_client.post("/api/analytics/event", json={
        "event_name": "page_view",
        "product_id": "desk-mat",
        "meta": {"source": "landing"}
    })
    assert res.status_code == 200
    assert "status" in res.json()
