import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_owner_stats_unauthorized(async_client: AsyncClient):
    """Ensure owner dashboard endpoint rejects requests without valid admin key."""
    res = await async_client.get("/api/owner/stats")
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_owner_stats_authorized(async_client: AsyncClient):
    """Ensure owner dashboard returns metrics when valid admin key is supplied."""
    res = await async_client.get("/api/owner/stats", headers={"X-Admin-Key": "storelab-admin-2026"})
    assert res.status_code == 200
    data = res.json()
    assert "total_signups" in data
    assert "signups_by_product" in data
    assert "analytics_events" in data
