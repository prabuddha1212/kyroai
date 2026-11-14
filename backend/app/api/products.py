from typing import List, Dict, Any
from fastapi import APIRouter
from app.db.supabase_client import supabase
from app.models.product import ALLOWED_PRODUCTS

router = APIRouter(tags=["products"])

@router.get("/products", response_model=List[Dict[str, Any]])
async def get_products():
    """
    Returns the active product catalogue.
    Tries Supabase 'products' table first; falls back gracefully to ALLOWED_PRODUCTS.
    """
    try:
        if supabase:
            response = supabase.table("products").select("*").execute()
            if response.data and len(response.data) > 0:
                # Filter active if column present
                return [p for p in response.data if p.get("is_active", True) is not False]
    except Exception:
        pass
    return ALLOWED_PRODUCTS
