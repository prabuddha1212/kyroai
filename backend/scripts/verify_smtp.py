"""Operational script to test SMTP email delivery."""
import os
import sys
from pathlib import Path

# Add backend root to sys.path so app can be imported
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.services.email_service import send_waitlist_confirmation_email

def main():
    print("=" * 60)
    print("Testing SMTP Credentials with configured mail provider...")
    print("=" * 60)

    test_recipient = os.getenv("TEST_EMAIL_RECIPIENT", "prabuddhakhedkar43@gmail.com")
    product = "Pure Black Desk Mat (XXL)"
    price = 799
    orig_price = 999

    success = send_waitlist_confirmation_email(
        to_email=test_recipient,
        product_name=product,
        product_price=price,
        original_price=orig_price,
        customer_name="Test Supporter"
    )

    if success:
        print(f"\n🎉 SUCCESS! A confirmation email was successfully handled for {test_recipient}.")
    else:
        print("\n❌ FAILED. Could not authenticate or connect to SMTP server.")

if __name__ == "__main__":
    main()
