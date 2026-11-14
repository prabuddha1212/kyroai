import time
from collections import defaultdict
from typing import Dict, List
from fastapi import HTTPException

# In-Memory IP Rate Limiting Store
_ip_rate_limits: Dict[str, List[float]] = defaultdict(list)

def check_rate_limit(client_ip: str, limit: int = 5, window_seconds: int = 60) -> None:
    """
    Checks if a given IP has exceeded the request threshold within the window.
    Raises HTTPException(429) if exceeded.
    """
    now = time.time()
    history = _ip_rate_limits[client_ip]
    _ip_rate_limits[client_ip] = [t for t in history if now - t < window_seconds]
    if len(_ip_rate_limits[client_ip]) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment before trying again."
        )
    _ip_rate_limits[client_ip].append(now)
