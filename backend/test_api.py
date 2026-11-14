# backend/test_api.py
"""
StoreLab Automated Test Suite
Uses Python asyncio, unittest and httpx.AsyncClient with mock DB.
"""
import sys
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).parent))

import unittest
import httpx
from main import app

class TestStoreLabAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.patcher = patch("router_waitlist.supabase")
        self.mock_sb = self.patcher.start()

        # Mock standard table query chains
        self.mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        self.mock_sb.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
        self.mock_sb.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])
        self.mock_sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        self.mock_sb.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock(data=[])

        self.transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=self.transport, base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        self.patcher.stop()

    async def test_health_check(self):
        """Verify the API health check endpoint returns 200 OK."""
        res = await self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"status": "ok"})

    async def test_get_products(self):
        """Verify products catalogue returns all 4 concept products with required fields."""
        res = await self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        products = res.json()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 4)

        for p in products:
            self.assertIn("id", p)
            self.assertIn("name", p)
            self.assertIn("price", p)
            self.assertIn("description", p)

    async def test_join_waitlist_invalid_email(self):
        """Ensure invalid email format is rejected with 422 validation error."""
        res = await self.client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "not-an-email"
        })
        self.assertEqual(res.status_code, 422)

    async def test_join_waitlist_invalid_product(self):
        """Ensure invalid product id is rejected with 400 Bad Request."""
        res = await self.client.post("/api/waitlist", json={
            "product_id": "non-existent-gear",
            "email": "valid@storelab.dev"
        })
        self.assertEqual(res.status_code, 400)

    async def test_join_waitlist_success(self):
        """Ensure valid submission records successfully."""
        res = await self.client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "alex@storelab.dev",
            "consent_given": True
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])

    async def test_anti_bot_honeypot(self):
        """Ensure honeypot traps bots and silently returns success without error."""
        res = await self.client.post("/api/waitlist", json={
            "product_id": "desk-mat",
            "email": "spambot@auto.com",
            "honeypot": "http://spam-link.ru"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])

    async def test_analytics_event_logging(self):
        """Ensure analytics events are captured."""
        res = await self.client.post("/api/analytics/event", json={"event_name": "page_view"})
        self.assertEqual(res.status_code, 200)

    async def test_owner_stats_unauthorized(self):
        """Ensure owner dashboard endpoint rejects requests without valid admin key."""
        res = await self.client.get("/api/owner/stats")
        self.assertEqual(res.status_code, 401)

    async def test_owner_stats_authorized(self):
        """Ensure owner dashboard returns metrics when valid admin key is supplied."""
        res = await self.client.get("/api/owner/stats", headers={"X-Admin-Key": "storelab-admin-2026"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_signups", data)
        self.assertIn("signups_by_product", data)

if __name__ == "__main__":
    unittest.main()
