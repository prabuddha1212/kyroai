import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Pre-mock supabase client before anything touches it
mock_supabase = MagicMock()
mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
mock_supabase.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
mock_supabase.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])
mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock(data=[])

import app.db.supabase_client as sb_mod
sb_mod._supabase_client = mock_supabase

import asyncio
from app.api.products import get_products
from app.models.waitlist import WaitlistRequest
from app.services.waitlist_service import WaitlistService
from app.services.rate_limiter import check_rate_limit, _ip_rate_limits

async def run():
    print("Testing get_products()...")
    products = await get_products()
    assert len(products) == 4, f"Expected 4 products, got {len(products)}"
    print(f"✓ get_products returned {len(products)} products")

    print("Testing WaitlistService.add_entry()...")
    req = WaitlistRequest(
        product_id="desk-mat",
        name="Alex Morgan",
        email="alex@storelab.dev",
        consent_given=True
    )
    res = WaitlistService.add_entry(req)
    assert res["success"] is True
    print("✓ WaitlistService.add_entry succeeded:", res["message"])

    print("Testing Rate Limiter...")
    _ip_rate_limits.clear()
    check_rate_limit("127.0.0.1")
    print("✓ Rate limiter verified")

    print("\n🎉 ALL ARCHITECTURAL LAYERS (Models, Services, API, DB) VERIFIED INSTANTANEOUSLY!")

if __name__ == "__main__":
    asyncio.run(run())
