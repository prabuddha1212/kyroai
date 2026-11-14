from typing import Optional
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from app.models.waitlist import WaitlistRequest, WaitlistResponse
from app.models.product import ALLOWED_PRODUCT_IDS
from app.services.rate_limiter import check_rate_limit
from app.services.waitlist_service import WaitlistService
from app.services.email_service import send_waitlist_confirmation_email

router = APIRouter(tags=["waitlist"])

@router.post("/waitlist", response_model=WaitlistResponse)
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
        return WaitlistResponse(success=True, message="Reservation confirmed!")

    # 2. Rate limiting check
    client_ip = http_req.client.host if http_req.client else "unknown"
    check_rate_limit(client_ip)

    # 3. Product validation
    if request.product_id not in ALLOWED_PRODUCT_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product. Allowed products: {', '.join(sorted(ALLOWED_PRODUCT_IDS))}"
        )

    clean_email = request.email.lower().strip()
    clean_name = request.name.strip() if request.name else "Early Supporter"

    prod = WaitlistService.get_product(request.product_id)
    prod_name = prod["name"] if prod else request.product_id
    prod_price = prod.get("price", 0) if prod else 0
    prod_orig_price = prod.get("original_price") if prod else None

    # 4. Check for duplicate signups
    is_duplicate = WaitlistService.check_duplicate(request.product_id, clean_email)
    if is_duplicate:
        # Re-send confirmation email without creating a duplicate record
        background_tasks.add_task(
            send_waitlist_confirmation_email,
            clean_email,
            prod_name,
            prod_price,
            prod_orig_price,
            clean_name
        )
        return WaitlistResponse(
            success=True,
            is_duplicate=True,
            message=f"Welcome back, {clean_name}! You are already registered for {prod_name}. A fresh confirmation email was dispatched."
        )

    # Queue confirmation email
    background_tasks.add_task(
        send_waitlist_confirmation_email,
        clean_email,
        prod_name,
        prod_price,
        prod_orig_price,
        clean_name
    )

    # 5. Persist
    result = WaitlistService.add_entry(request)
    return WaitlistResponse(**result)


@router.delete("/waitlist")
async def delete_waitlist_entry(email: str, product_id: Optional[str] = None):
    """
    Privacy compliance endpoint: Delete customer registration by email.
    """
    return WaitlistService.delete_entry(email, product_id)
