import re
from typing import Optional, Any
from pydantic import BaseModel, field_validator

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


class WaitlistResponse(BaseModel):
    success: bool
    message: str
    is_duplicate: Optional[bool] = False
    data: Optional[Any] = None
