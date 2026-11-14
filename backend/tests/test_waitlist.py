import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_join_waitlist_success(async_client: AsyncClient):
    """Ensure valid submission records successfully."""
    res = await async_client.post("/api/waitlist", json={
        "product_id": "desk-mat",
        "name": "Alex Morgan",
        "email": "alex@storelab.dev",
        "consent_given": True
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True

@pytest.mark.asyncio
async def test_join_waitlist_invalid_email(async_client: AsyncClient):
    """Ensure invalid email format is rejected with 422 validation error."""
    res = await async_client.post("/api/waitlist", json={
        "product_id": "desk-mat",
        "email": "not-an-email"
    })
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_join_waitlist_invalid_product(async_client: AsyncClient):
    """Ensure invalid product id is rejected with 400 Bad Request."""
    res = await async_client.post("/api/waitlist", json={
        "product_id": "non-existent-gear",
        "email": "valid@storelab.dev"
    })
    assert res.status_code == 400

@pytest.mark.asyncio
async def test_anti_bot_honeypot(async_client: AsyncClient):
    """Ensure honeypot traps bots and silently returns success without error."""
    res = await async_client.post("/api/waitlist", json={
        "product_id": "desk-mat",
        "email": "spambot@auto.com",
        "honeypot": "http://spam-link.ru"
    })
    assert res.status_code == 200
    assert res.json()["success"] is True
