"""
StoreLab Automated Test Suite (Unittest + AsyncIO)
Verifies the new layered architecture: app.main, app.api, app.services, app.models.
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import httpx
from app.main import app
from app.services.rate_limiter import check_rate_limit, _ip_rate_limits
from app.models.product import ALLOWED_PRODUCTS, ALLOWED_PRODUCT_IDS
from app.models.waitlist import WaitlistRequest
from fastapi import HTTPException
from pydantic import ValidationError

class TestStoreLabNewArchitecture(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_sb = MagicMock()
        self.mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        self.mock_sb.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
        self.mock_sb.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])
        self.mock_sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        self.mock_sb.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock(data=[])

        self.patchers = [
            patch("app.db.supabase_client.supabase", self.mock_sb),
            patch("app.services.waitlist_service.supabase", self.mock_sb),
            patch("app.services.analytics_service.supabase", self.mock_sb),
            patch("app.api.products.supabase", self.mock_sb),
            patch("app.api.waitlist.send_waitlist_confirmation_email", MagicMock(return_value=True)),
        ]
        for p in self.patchers:
            p.start()

        self.transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=self.transport, base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        for p in self.patchers:
            p.stop()

    async def test_health_check(self):
        res = await self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"status": "ok"})

    async def test_get_products(self):
        res = await self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 4)
        for p in data:
            self.assertIn("id", p)
            self.assertIn("name", p)
            self.assertIn("price", p)

    async def test_join_waitlist_success(self):
        res = await self.client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "consent_given": True
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])

    async def test_join_waitlist_invalid_email(self):
        res = await self.client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "invalid-email"
        })
        self.assertEqual(res.status_code, 422)

    async def test_join_waitlist_invalid_product(self):
        res = await self.client.post("/api/waitlist", json={
            "product_id": "fake-gear",
            "email": "valid@storelab.dev"
        })
        self.assertEqual(res.status_code, 400)

    async def test_anti_bot_honeypot(self):
        res = await self.client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "bot@spam.com",
            "honeypot": "https://spam.ru"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])

    async def test_owner_stats_unauthorized(self):
        res = await self.client.get("/api/owner/stats")
        self.assertEqual(res.status_code, 401)

    async def test_owner_stats_authorized(self):
        res = await self.client.get("/api/owner/stats", headers={"X-Admin-Key": "storelab-admin-2026"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_signups", data)
        self.assertIn("signups_by_product", data)


class TestServicesAndModels(unittest.TestCase):
    def setUp(self):
        _ip_rate_limits.clear()

    def test_products_catalog(self):
        self.assertEqual(len(ALLOWED_PRODUCTS), 4)
        for p in ALLOWED_PRODUCTS:
            self.assertIn(p["id"], ALLOWED_PRODUCT_IDS)

    def test_rate_limiter(self):
        ip = "127.0.0.1"
        for _ in range(5):
            check_rate_limit(ip, limit=5, window_seconds=60)
        with self.assertRaises(HTTPException):
            check_rate_limit(ip, limit=5, window_seconds=60)

    def test_model_validation(self):
        with self.assertRaises(ValidationError):
            WaitlistRequest(product_id="desk-mat", email="bad")


if __name__ == "__main__":
    unittest.main(verbosity=2)
