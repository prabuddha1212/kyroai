# backend/verify_smtp.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from email_service import send_waitlist_confirmation_email

print("=" * 60)
print("Testing SMTP Credentials with Gmail...")
print("=" * 60)

test_recipient = "prabuddhakhedkar43@gmail.com"
product = "Pure Black Desk Mat (XXL)"
price = 799
orig_price = 999

success = send_waitlist_confirmation_email(
    to_email=test_recipient,
    product_name=product,
    product_price=price,
    original_price=orig_price
)

if success:
    print(f"\n🎉 SUCCESS! A test confirmation email was successfully sent to {test_recipient}.")
    print("Check your Gmail inbox (and spam/promotions folder just in case).")
else:
    print("\n❌ FAILED. Could not authenticate or connect to smtp.gmail.com.")

