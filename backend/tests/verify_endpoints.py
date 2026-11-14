import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
import httpx

async def test_all():
    mock_sb = MagicMock()
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
    mock_sb.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])
    mock_sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])

    patch("app.db.supabase_client.supabase", mock_sb).start()
    patch("app.services.waitlist_service.supabase", mock_sb).start()
    patch("app.services.analytics_service.supabase", mock_sb).start()
    patch("app.api.products.supabase", mock_sb).start()
    patch("app.api.waitlist.send_waitlist_confirmation_email", MagicMock(return_value=True)).start()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health
        res = await client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.status_code}"
        print("✓ /health passed (200)")

        # 2. Products
        res = await client.get("/api/products")
        assert res.status_code == 200, f"Products check failed: {res.status_code}"
        products = res.json()
        assert len(products) >= 4, "Less than 4 products returned"
        print(f"✓ /api/products passed (200, {len(products)} products)")

        # 3. Waitlist success
        res = await client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "name": "Alex",
            "email": "alex@storelab.dev",
            "consent_given": True
        })
        assert res.status_code == 200, f"Waitlist signup failed: {res.status_code}"
        print("✓ /api/waitlist signup passed (200)")

        # 4. Waitlist invalid email
        res = await client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "bad-email"
        })
        assert res.status_code == 422, f"Expected 422, got {res.status_code}"
        print("✓ /api/waitlist validation 422 passed")

        # 5. Anti-bot honeypot
        res = await client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "bot@spam.com",
            "honeypot": "https://spambot.ru"
        })
        assert res.status_code == 200, f"Honeypot failed: {res.status_code}"
        print("✓ Anti-bot honeypot trap passed (200)")

        # 6. Owner stats authorized
        res = await client.get("/api/owner/stats", headers={"X-Admin-Key": "storelab-admin-2026"})
        assert res.status_code == 200, f"Owner stats failed: {res.status_code}"
        print("✓ /api/owner/stats authorized passed (200)")

        # 7. Owner stats unauthorized
        res = await client.get("/api/owner/stats")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("✓ /api/owner/stats unauthorized 401 passed")

    print("\n🎉 ALL BACKEND ENDPOINTS AND ARCHITECTURE VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(test_all())
