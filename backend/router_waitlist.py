# backend/router_waitlist.py
import re
import os
import time
from collections import defaultdict
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Request, Header, BackgroundTasks
from pydantic import BaseModel, field_validator
from .supabase_client import supabase
from .email_service import send_waitlist_confirmation_email

router = APIRouter(prefix="/api", tags=["waitlist"])

# -----------------------------------------------------------------------------
# 1. Product Catalogue (Backend as Single Source of Truth)
# -----------------------------------------------------------------------------
ALLOWED_PRODUCTS = [
    {
        "id": "desk-mat",
        "name": "Pure Black Desk Mat (XXL)",
        "tagline": "Spacious water-resistant surface with anti-fray stitching",
        "price": 799,
        "original_price": 999,
        "category": "Surface",
        "badge": "Early Bird",
        "image_url": "https://images.unsplash.com/photo-1616440347437-b1c73416efc2?auto=format&fit=crop&w=800&q=80",
        "description": "Engineered for precision tracking and desk protection. Premium micro-textured cloth with high-density stitched borders and non-slip rubber backing.",
        "features": ["900mm x 400mm x 4mm", "Water-resistant coating", "Non-slip rubber base"]
    },
    {
        "id": "headphone-stand",
        "name": "Solid Aluminum Headphone Stand",
        "tagline": "Minimalist weighted cradle for premium audio gear",
        "price": 599,
        "original_price": 799,
        "category": "Organizer",
        "badge": "Popular",
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80",
        "description": "Keep your desk clutter-free while protecting your headband. CNC-milled aluminum with curved silicone rest and anti-slip silicone feet.",
        "features": ["Weighted steel base", "Curved protective silicone", "Matte anodized black finish"]
    },
    {
        "id": "cable-kit",
        "name": "Zen Magnetic Cable Management Pack",
        "tagline": "Magnetic clips & routing channels to tame loose wires",
        "price": 399,
        "original_price": 599,
        "category": "Cables",
        "badge": "Essential",
        "image_url": "https://images.unsplash.com/photo-1588508065123-287b28e013da?auto=format&fit=crop&w=800&q=80",
        "description": "Eliminate charging cable drop-offs and messy desktop wires. Magnetic snap collars attach to desk edge mount strips for single-handed docking.",
        "features": ["5x Magnetic clips", "3x Under-desk channels", "Damage-free 3M adhesive"]
    },
    {
        "id": "keyboard",
        "name": "Custom 75% Mechanical Keyboard",
        "tagline": "Hot-swappable linear switches with acoustic dampening",
        "price": 2999,
        "original_price": 3999,
        "category": "Hardware",
        "badge": "Flagship",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
        "description": "Pre-lubed smooth linear switches, sound-dampening silicone gaskets, and per-key RGB in a compact 75% desk-saving layout.",
        "features": ["Hot-swappable 5-pin sockets", "Gasket-mounted acoustic dampening", "Detachable braided Type-C"]
    }
]

ALLOWED_PRODUCT_IDS = {p["id"] for p in ALLOWED_PRODUCTS}

# -----------------------------------------------------------------------------
# 2. In-Memory Fallback Tracking & Rate Limiting
# -----------------------------------------------------------------------------
_ip_rate_limits: Dict[str, List[float]] = defaultdict(list)
_in_memory_waitlist: List[Dict[str, Any]] = []
_in_memory_analytics: List[Dict[str, Any]] = []

def check_rate_limit(client_ip: str, limit: int = 5, window_seconds: int = 60):
    now = time.time()
    history = _ip_rate_limits[client_ip]
    _ip_rate_limits[client_ip] = [t for t in history if now - t < window_seconds]
    if len(_ip_rate_limits[client_ip]) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a moment before trying again."
        )
    _ip_rate_limits[client_ip].append(now)


# -----------------------------------------------------------------------------
# 3. Request / Response Models
# -----------------------------------------------------------------------------
class WaitlistRequest(BaseModel):
    product_id: str
    email: str
    name: Optional[str] = ""
    consent_given: bool = True
    honeypot: Optional[str] = None  # Spam bots fill this hidden field

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", clean):
            raise ValueError("Please provide a valid email address (e.g. name@domain.com)")
        return clean

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> str:
        if v:
            clean = v.strip()
            if len(clean) > 80:
                return clean[:80]
            return clean
        return ""


class AnalyticsEventRequest(BaseModel):
    event_name: str
    product_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


# -----------------------------------------------------------------------------
# 4. API Endpoints
# -----------------------------------------------------------------------------
@router.get("/products")
async def get_products():
    """
    Returns the active product catalogue.
    Tries Supabase 'products' table first; falls back gracefully to ALLOWED_PRODUCTS.
    """
    try:
        response = supabase.table("products").select("*").execute()
        if response.data and len(response.data) > 0:
            # Filter active if column present
            return [p for p in response.data if p.get("is_active", True) is not False]
    except Exception:
        pass
    return ALLOWED_PRODUCTS


@router.post("/waitlist")
async def join_waitlist(
    request: WaitlistRequest,
    http_req: Request,
    background_tasks: BackgroundTasks
):
    """
    Join the product waitlist with input validation, duplicate prevention,
    bot traps, and automated email confirmation.
    """
    # 1. Anti-Bot Honeypot check
    if request.honeypot:
        return {"success": True, "message": "Reservation confirmed!"}

    # 2. Rate limiting check
    client_ip = http_req.client.host if http_req.client else "unknown"
    check_rate_limit(client_ip)

    # 3. Product validation
    if request.product_id not in ALLOWED_PRODUCT_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product. Allowed products: {', '.join(ALLOWED_PRODUCT_IDS)}"
        )

    clean_email = request.email.lower().strip()
    clean_name = request.name.strip() if request.name else "Early Supporter"

    # Find product details for email & responses
    prod = next((p for p in ALLOWED_PRODUCTS if p["id"] == request.product_id), None)
    prod_name = prod["name"] if prod else request.product_id
    prod_price = prod.get("price", 0) if prod else 0
    prod_orig_price = prod.get("original_price") if prod else None

    # 4. Check for duplicate signups first (prevent duplicate rows in Supabase)
    is_duplicate = False
    try:
        existing = (
            supabase.table("waitlist")
            .select("id")
            .eq("product_id", request.product_id)
            .eq("email", clean_email)
            .execute()
        )
        if existing.data and len(existing.data) > 0:
            is_duplicate = True
    except Exception:
        # Check in-memory fallback for duplicate
        if any(item["product_id"] == request.product_id and item["email"] == clean_email for item in _in_memory_waitlist):
            is_duplicate = True

    if is_duplicate:
        # Re-send confirmation email without creating a duplicate record
        background_tasks.add_task(
            send_waitlist_confirmation_email,
            clean_email,
            prod_name,
            prod_price,
            prod_orig_price
        )
        return {
            "success": True,
            "is_duplicate": True,
            "message": f"Welcome back, {clean_name}! You are already registered for {prod_name}. A fresh confirmation email was dispatched."
        }

    # Queue confirmation email
    background_tasks.add_task(
        send_waitlist_confirmation_email,
        clean_email,
        prod_name,
        prod_price,
        prod_orig_price
    )

    # 5. Persist to Supabase
    try:
        # Build payload dynamically based on schema
        payload = {
            "product_id": request.product_id,
            "email": clean_email,
            "name": clean_name,
            "consent_given": request.consent_given
        }

        try:
            response = supabase.table("waitlist").insert(payload).execute()
        except Exception as insert_err:
            # If 'name' or 'consent_given' column doesn't exist yet in Supabase, retry with basic fields
            err_str = str(insert_err)
            if "PGRST204" in err_str or "column" in err_str.lower():
                response = supabase.table("waitlist").insert({
                    "product_id": request.product_id,
                    "email": clean_email
                }).execute()
            else:
                raise insert_err

        # Log analytics conversion
        try:
            supabase.table("analytics_events").insert({
                "event_name": "waitlist_success",
                "product_id": request.product_id,
                "meta": {"email_domain": clean_email.split("@")[-1], "name": clean_name}
            }).execute()
        except Exception:
            _in_memory_analytics.append({
                "event_name": "waitlist_success",
                "product_id": request.product_id
            })

        return {
            "success": True,
            "message": f"Spot reserved! Welcome to early access, {clean_name}. A confirmation email has been sent to {clean_email}.",
            "data": response.data
        }
    except Exception as e:
        error_msg = str(e)
        if "23505" in error_msg or "duplicate" in error_msg.lower():
            return {
                "success": True,
                "is_duplicate": True,
                "message": f"You are already on the waitlist for {prod_name}!"
            }

        # In-memory fallback if Supabase is offline
        _in_memory_waitlist.append({
            "product_id": request.product_id,
            "email": clean_email,
            "name": clean_name,
            "created_at": time.time(),
            "consent_given": request.consent_given
        })
        return {
            "success": True,
            "message": f"Spot reserved! Confirmation email dispatched to {clean_email}."
        }


@router.post("/analytics/event")
async def record_analytics_event(payload: AnalyticsEventRequest):
    """
    Records an analytics event (page views, button clicks, conversions).
    """
    event_data = {
        "event_name": payload.event_name,
        "product_id": payload.product_id,
        "meta": payload.meta or {}
    }
    try:
        supabase.table("analytics_events").insert(event_data).execute()
        return {"status": "recorded"}
    except Exception:
        _in_memory_analytics.append(event_data)
        return {"status": "recorded_locally"}


@router.get("/owner/stats")
async def get_owner_stats(x_admin_key: Optional[str] = Header(None)):
    """
    Owner dashboard stats endpoint.
    Protected by secret key in X-Admin-Key header.
    """
    admin_secret = os.getenv("ADMIN_KEY", "storelab-admin-2026")
    if not x_admin_key or x_admin_key != admin_secret:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Admin Key")

    product_signups: Dict[str, int] = {p["id"]: 0 for p in ALLOWED_PRODUCTS}
    recent_signups = []

    # 1. Fetch waitlist from Supabase
    try:
        waitlist_res = supabase.table("waitlist").select("*").order("created_at", desc=True).limit(100).execute()
        if waitlist_res.data:
            for row in waitlist_res.data:
                pid = row.get("product_id")
                if pid in product_signups:
                    product_signups[pid] += 1
                recent_signups.append({
                    "id": row.get("id"),
                    "name": row.get("name") or "Supporter",
                    "email": row.get("email"),
                    "product_id": pid,
                    "created_at": row.get("created_at")
                })
    except Exception:
        pass

    # Merge in-memory fallback entries if any
    for row in _in_memory_waitlist:
        pid = row["product_id"]
        if pid in product_signups:
            product_signups[pid] += 1
        recent_signups.append({
            "name": row.get("name") or "Supporter",
            "email": row.get("email"),
            "product_id": pid,
            "created_at": "Just now"
        })

    # 2. Fetch analytics event counts
    event_counts: Dict[str, int] = defaultdict(int)
    try:
        analytics_res = supabase.table("analytics_events").select("event_name").execute()
        if analytics_res.data:
            for row in analytics_res.data:
                event_counts[row.get("event_name")] += 1
    except Exception:
        pass

    for ev in _in_memory_analytics:
        event_counts[ev["event_name"]] += 1

    return {
        "total_signups": sum(product_signups.values()),
        "signups_by_product": product_signups,
        "analytics_events": dict(event_counts),
        "recent_signups": recent_signups[:30]
    }


@router.delete("/waitlist")
async def delete_waitlist_entry(email: str, product_id: Optional[str] = None):
    """
    Privacy compliance endpoint: Delete customer registration by email.
    """
    clean_email = email.lower().strip()
    try:
        query = supabase.table("waitlist").delete().eq("email", clean_email)
        if product_id:
            query = query.eq("product_id", product_id)
        res = query.execute()
        return {"success": True, "message": f"Successfully removed {clean_email} from waitlist."}
    except Exception:
        global _in_memory_waitlist
        _in_memory_waitlist = [item for item in _in_memory_waitlist if item["email"] != clean_email]
        return {"success": True, "message": f"Waitlist deletion recorded for {clean_email}."}
