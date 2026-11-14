from __future__ import annotations
from typing import Any, Optional
from supabase import create_client, Client
from app.config import settings

_supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            _supabase_client = create_client("https://dummy.supabase.co", "dummy-key")
        else:
            _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _supabase_client

class _SupabaseProxy:
    def __getattr__(self, name: str) -> Any:
        client = get_supabase_client()
        return getattr(client, name)

    def __bool__(self) -> bool:
        return bool(settings.SUPABASE_URL and settings.SUPABASE_KEY)

supabase: Client = _SupabaseProxy()  # type: ignore


def test_connection() -> dict[str, Any]:
    """
    Sanity-check Supabase connectivity.
    """
    client = get_supabase_client()
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise EnvironmentError(
            "Supabase credentials not found. Ensure SUPABASE_URL and SUPABASE_KEY are set in .env"
        )

    # 1. Verify connection to Supabase services
    client.auth.get_session()

    # 2. Check if the 'products' table exists
    try:
        response = client.table("products").select("*").limit(5).execute()
        return {
            "connected": True,
            "table_exists": True,
            "data": response.data,
        }
    except Exception as e:
        error_msg = str(e)
        if "PGRST205" in error_msg:
            return {
                "connected": True,
                "table_exists": False,
                "message": "Connected to Supabase! The 'products' table does not exist in your database yet.",
            }
        raise e
