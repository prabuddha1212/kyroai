from unittest.mock import MagicMock, patch
import pytest
import httpx
from app.main import app

@pytest.fixture(autouse=True)
def mock_supabase():
    """Mock Supabase table calls for hermetic testing."""
    with patch("app.db.supabase_client.supabase") as mock_sb:
        mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        mock_sb.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
        mock_sb.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])
        mock_sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])
        mock_sb.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
        yield mock_sb

@pytest.fixture
async def async_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
