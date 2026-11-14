import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_products(async_client: AsyncClient):
    """Verify products catalogue returns all 4 concept products with required fields."""
    res = await async_client.get("/api/products")
    assert res.status_code == 200
    products = res.json()
    assert isinstance(products, list)
    assert len(products) >= 4

    for p in products:
        assert "id" in p
        assert "name" in p
        assert "price" in p
        assert "description" in p
