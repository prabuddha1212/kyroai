# backend/supabase_client.py
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, List

from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env (the file lives next to this module)
env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

_SUPABASE_URL = os.getenv("SUPABASE_URL")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not _SUPABASE_URL or not _SUPABASE_KEY:
    raise EnvironmentError(
        "Supabase credentials not found. Ensure SUPABASE_URL and SUPABASE_KEY are set in .env"
    )

# Re‑usable client instance
supabase: Client = create_client(_SUPABASE_URL, _SUPABASE_KEY)


def test_connection() -> dict[str, Any]:
    """
    Sanity-check Supabase connectivity.
    """
    # 1. Verify connection to Supabase services
    supabase.auth.get_session()

    # 2. Check if the 'products' table exists
    try:
        response = supabase.table("products").select("*").limit(5).execute()
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