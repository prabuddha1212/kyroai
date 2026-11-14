import pytest
from fastapi import HTTPException
from app.services.rate_limiter import check_rate_limit, _ip_rate_limits

def setup_function():
    _ip_rate_limits.clear()

def test_rate_limiter_allows_under_threshold():
    """Verify requests under rate limit threshold pass."""
    test_ip = "192.168.1.100"
    for _ in range(4):
        check_rate_limit(test_ip, limit=5, window_seconds=60)
    assert len(_ip_rate_limits[test_ip]) == 4

def test_rate_limiter_blocks_above_threshold():
    """Verify exceeding threshold triggers HTTP 429 Too Many Requests."""
    test_ip = "192.168.1.200"
    for _ in range(5):
        check_rate_limit(test_ip, limit=5, window_seconds=60)

    with pytest.raises(HTTPException) as exc_info:
        check_rate_limit(test_ip, limit=5, window_seconds=60)
    assert exc_info.value.status_code == 429
