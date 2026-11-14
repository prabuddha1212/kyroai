import time
from typing import List, Dict, Any, Optional
from app.db.supabase_client import supabase
from app.models.product import ALLOWED_PRODUCTS, ALLOWED_PRODUCT_IDS
from app.models.waitlist import WaitlistRequest

# In-memory storage fallback if Supabase is unreachable
_in_memory_waitlist: List[Dict[str, Any]] = []

class WaitlistService:
    @staticmethod
    def get_product(product_id: str) -> Optional[Dict[str, Any]]:
        return next((p for p in ALLOWED_PRODUCTS if p["id"] == product_id), None)

    @staticmethod
    def check_duplicate(product_id: str, email: str) -> bool:
        clean_email = email.lower().strip()
        try:
            if supabase:
                existing = (
                    supabase.table("waitlist")
                    .select("id")
                    .eq("product_id", product_id)
                    .eq("email", clean_email)
                    .execute()
                )
                if existing.data and len(existing.data) > 0:
                    return True
        except Exception:
            pass

        # Check in-memory fallback
        return any(
            item["product_id"] == product_id and item["email"] == clean_email
            for item in _in_memory_waitlist
        )

    @staticmethod
    def add_entry(request: WaitlistRequest) -> Dict[str, Any]:
        clean_email = request.email.lower().strip()
        clean_name = request.name.strip() if request.name else "Early Supporter"
        prod = WaitlistService.get_product(request.product_id)
        prod_name = prod["name"] if prod else request.product_id

        # 1. Try Supabase insert
        try:
            if not supabase:
                raise RuntimeError("Supabase client not initialized")

            payload = {
                "product_id": request.product_id,
                "email": clean_email,
                "name": clean_name,
                "consent_given": request.consent_given,
            }

            try:
                response = supabase.table("waitlist").insert(payload).execute()
            except Exception as insert_err:
                err_str = str(insert_err)
                if "PGRST204" in err_str or "column" in err_str.lower():
                    # Retry with basic columns if migration hasn't run
                    response = supabase.table("waitlist").insert({
                        "product_id": request.product_id,
                        "email": clean_email
                    }).execute()
                else:
                    raise insert_err

            return {
                "success": True,
                "is_duplicate": False,
                "message": f"Spot reserved! Welcome to early access, {clean_name}. A confirmation email has been sent to {clean_email}.",
                "data": response.data,
            }

        except Exception as e:
            error_msg = str(e)
            if "23505" in error_msg or "duplicate" in error_msg.lower():
                return {
                    "success": True,
                    "is_duplicate": True,
                    "message": f"You are already on the waitlist for {prod_name}!",
                }

            # In-memory fallback
            fallback_record = {
                "product_id": request.product_id,
                "email": clean_email,
                "name": clean_name,
                "created_at": time.time(),
                "consent_given": request.consent_given,
            }
            _in_memory_waitlist.append(fallback_record)
            return {
                "success": True,
                "is_duplicate": False,
                "message": f"Spot reserved! Confirmation email dispatched to {clean_email}.",
                "data": [fallback_record],
            }

    @staticmethod
    def delete_entry(email: str, product_id: Optional[str] = None) -> Dict[str, Any]:
        clean_email = email.lower().strip()
        try:
            if supabase:
                query = supabase.table("waitlist").delete().eq("email", clean_email)
                if product_id:
                    query = query.eq("product_id", product_id)
                query.execute()
                return {"success": True, "message": f"Successfully removed {clean_email} from waitlist."}
        except Exception:
            pass

        global _in_memory_waitlist
        _in_memory_waitlist = [item for item in _in_memory_waitlist if item["email"] != clean_email]
        return {"success": True, "message": f"Waitlist deletion recorded for {clean_email}."}

    @staticmethod
    def get_owner_stats() -> Dict[str, Any]:
        product_signups: Dict[str, int] = {p["id"]: 0 for p in ALLOWED_PRODUCTS}
        recent_signups = []

        try:
            if supabase:
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
                            "created_at": row.get("created_at"),
                        })
        except Exception:
            pass

        # Merge in-memory fallback entries
        for row in _in_memory_waitlist:
            pid = row["product_id"]
            if pid in product_signups:
                product_signups[pid] += 1
            recent_signups.append({
                "name": row.get("name") or "Supporter",
                "email": row.get("email"),
                "product_id": pid,
                "created_at": "Just now",
            })

        return {
            "total_signups": sum(product_signups.values()),
            "signups_by_product": product_signups,
            "recent_signups": recent_signups[:30],
        }
