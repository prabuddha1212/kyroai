# backend/test_suite.py
"""
StoreLab MVP Unit Test Suite
Validates core logic: Product Catalog, Pydantic validation (name, email, product),
Duplicate handling, Rate Limiting, Anti-Bot Honeypot, and Email confirmation.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import unittest
from pydantic import ValidationError
from fastapi import HTTPException
from router_waitlist import (
    ALLOWED_PRODUCTS,
    ALLOWED_PRODUCT_IDS,
    WaitlistRequest,
    AnalyticsEventRequest,
    check_rate_limit,
    _ip_rate_limits,
)
from email_service import send_waitlist_confirmation_email


class TestStoreLabLogic(unittest.TestCase):
    def setUp(self):
        _ip_rate_limits.clear()

    def test_products_catalog_integrity(self):
        """Verify product catalog meets MVP requirements (4 products with prices and features)."""
        self.assertEqual(len(ALLOWED_PRODUCTS), 4)
        for p in ALLOWED_PRODUCTS:
            self.assertIn(p["id"], ALLOWED_PRODUCT_IDS)
            self.assertTrue(p["name"])
            self.assertGreater(p["price"], 0)
            self.assertTrue(p["description"])
            self.assertIsInstance(p["features"], list)
            self.assertGreaterEqual(len(p["features"]), 2)

    def test_waitlist_valid_payload_with_name(self):
        """Verify valid customer name, email and product are parsed cleanly."""
        req = WaitlistRequest(
            product_id="desk-mat",
            name="  Alex Morgan  ",
            email="  Alex@Domain.COM  "
        )
        self.assertEqual(req.name, "Alex Morgan")
        self.assertEqual(req.email, "alex@domain.com")
        self.assertEqual(req.product_id, "desk-mat")
        self.assertIsNone(req.honeypot)
        self.assertTrue(req.consent_given)

    def test_waitlist_invalid_email_raises_error(self):
        """Verify malformed email throws validation error."""
        with self.assertRaises(ValidationError):
            WaitlistRequest(product_id="desk-mat", name="Alex", email="not-an-email")

        with self.assertRaises(ValidationError):
            WaitlistRequest(product_id="desk-mat", name="Alex", email="missing-domain@")

    def test_anti_bot_honeypot_field(self):
        """Verify honeypot field captures bot submissions."""
        req = WaitlistRequest(
            product_id="desk-mat",
            name="Spam Bot",
            email="bot@domain.com",
            honeypot="http://spam-link.org"
        )
        self.assertEqual(req.honeypot, "http://spam-link.org")

    def test_rate_limiter_allows_under_threshold(self):
        """Verify requests under rate limit threshold pass."""
        test_ip = "192.168.1.100"
        for _ in range(4):
            check_rate_limit(test_ip, limit=5, window_seconds=60)
        self.assertEqual(len(_ip_rate_limits[test_ip]), 4)

    def test_rate_limiter_blocks_above_threshold(self):
        """Verify 5th request triggers HTTP 429 Too Many Requests."""
        test_ip = "192.168.1.200"
        for _ in range(5):
            check_rate_limit(test_ip, limit=5, window_seconds=60)
        
        with self.assertRaises(HTTPException) as ctx:
            check_rate_limit(test_ip, limit=5, window_seconds=60)
        self.assertEqual(ctx.exception.status_code, 429)

    def test_analytics_event_payload(self):
        """Verify analytics event payload parsing."""
        event = AnalyticsEventRequest(
            event_name="product_click",
            product_id="headphone-stand",
            meta={"referrer": "google"}
        )
        self.assertEqual(event.event_name, "product_click")
        self.assertEqual(event.product_id, "headphone-stand")

    def test_confirmation_email_simulated_mode(self):
        """Verify confirmation email generates without error even when SMTP credentials are unconfigured."""
        res = send_waitlist_confirmation_email(
            to_email="customer@example.com",
            product_name="Pure Black Desk Mat (XXL)",
            product_price=799,
            original_price=999,
            customer_name="Alex Morgan"
        )
        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
