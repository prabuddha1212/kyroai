"""
StoreLab Transactional Email Service
Sends confirmation emails when visitors join the waitlist.
Uses Python's built-in smtplib so zero external pip packages are needed.
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from app.config import settings


def send_waitlist_confirmation_email(
    to_email: str,
    product_name: str,
    product_price: int,
    original_price: Optional[int] = None,
    customer_name: Optional[str] = None
) -> bool:
    """
    Sends a personalized branded confirmation email to a newly enrolled waitlist user.
    Runs asynchronously in FastAPI BackgroundTasks so API responses stay instantaneous.
    """
    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD
    from_email = settings.SMTP_FROM_EMAIL

    name_greeting = customer_name.strip() if customer_name and customer_name.strip() else "Early Supporter"
    subject = f"You're on the waitlist for {product_name} 🚀"

    # Plain text version
    text_content = f"""
Hello {name_greeting},

Thanks for your interest in StoreLab!

You have successfully reserved early access for:
Product: {product_name}
Target Price: ₹{product_price:,} (Zero upfront payment required)

What happens next?
1. We are testing community demand and refining the physical prototype.
2. Once the first batch is ready, you will receive priority access 48 hours before public release.
3. You will receive an exclusive early-bird reservation discount.

If you ever wish to be removed from this list, simply reply to this email or visit our privacy portal.

Best regards,
The StoreLab Team
https://storelab.dev
"""

    price_html = f"₹{product_price:,}"
    if original_price:
        price_html += f" <span style='text-decoration: line-through; color: #737373; font-size: 14px;'>₹{original_price:,}</span>"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0a0a0a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #ededed;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0a0a0a; padding: 40px 20px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width: 560px; background-color: #141414; border: 1px solid #262626; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.4);" cellspacing="0" cellpadding="0">
          
          <!-- Header -->
          <tr>
            <td style="padding: 28px 32px; border-bottom: 1px solid #262626; background: linear-gradient(180deg, #181818 0%, #141414 100%);">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td>
                    <div style="display: inline-block; width: 36px; height: 36px; line-height: 36px; text-align: center; border-radius: 10px; background: linear-gradient(135deg, #10d68f, #059669); color: #000; font-weight: 800; font-size: 18px; margin-right: 10px; vertical-align: middle;">S</div>
                    <span style="font-size: 20px; font-weight: 700; color: #ffffff; vertical-align: middle; letter-spacing: -0.5px;">StoreLab</span>
                  </td>
                  <td align="right">
                    <span style="display: inline-block; padding: 4px 10px; border-radius: 99px; background-color: rgba(16, 214, 143, 0.1); border: 1px solid rgba(16, 214, 143, 0.3); color: #10d68f; font-size: 11px; font-weight: 600; text-transform: uppercase;">Early Access</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Main Body -->
          <tr>
            <td style="padding: 36px 32px;">
              <h1 style="margin: 0 0 12px 0; font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
                You're on the waitlist, {name_greeting}! 🎉
              </h1>
              <p style="margin: 0 0 28px 0; font-size: 15px; line-height: 1.6; color: #a3a3a3;">
                Thanks for supporting indie hardware development. Your reservation spot has been securely confirmed with zero upfront charges.
              </p>

              <!-- Product Reservation Card -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #1a1a1a; border: 1px solid #2e2e2e; border-radius: 12px; margin-bottom: 28px;">
                <tr>
                  <td style="padding: 20px 24px;">
                    <span style="font-size: 11px; text-transform: uppercase; color: #10d68f; font-weight: 700; letter-spacing: 0.5px;">Reserved Concept</span>
                    <h3 style="margin: 6px 0 10px 0; font-size: 18px; font-weight: 700; color: #ffffff;">{product_name}</h3>
                    <div style="font-size: 20px; font-weight: 800; color: #ffffff;">
                      {price_html}
                      <span style="font-size: 12px; font-weight: 400; color: #a3a3a3; margin-left: 8px;">• No payment until shipping</span>
                    </div>
                  </td>
                </tr>
              </table>

              <!-- Steps -->
              <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.5px;">
                What happens next?
              </h4>
              <ol style="margin: 0 0 28px 0; padding-left: 20px; font-size: 14px; line-height: 1.7; color: #a3a3a3;">
                <li style="margin-bottom: 6px;">We validate demand across the gaming and creator community.</li>
                <li style="margin-bottom: 6px;">You will receive prototype progress updates and early feedback surveys.</li>
                <li>When physical production units are ready, you receive a <strong>private 48-hour order window</strong> before public release.</li>
              </ol>

              <!-- CTA Button -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <a href="http://localhost:3000/storelab-3d" style="display: inline-block; background-color: #10d68f; color: #04140e; text-decoration: none; padding: 12px 28px; border-radius: 10px; font-weight: 700; font-size: 14px;">
                      View Product in 3D Studio →
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding: 24px 32px; background-color: #0d0d0d; border-top: 1px solid #222222; text-align: center; font-size: 12px; color: #666666; line-height: 1.5;">
              <p style="margin: 0 0 6px 0;">StoreLab • Next.js + FastAPI + Supabase</p>
              <p style="margin: 0;">You received this email because you signed up for early access at {to_email}. You can request data removal anytime.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    if not smtp_host or not smtp_user or not smtp_password:
        print("\n" + "=" * 60)
        print("📨 [STORELAB EMAIL SERVICE — SIMULATED MODE]")
        print(f"To:      {to_email} ({name_greeting})")
        print(f"Subject: {subject}")
        print(f"Product: {product_name} (₹{product_price:,})")
        print("=" * 60 + "\n")
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        if smtp_port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=10) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.ehlo()
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.ehlo()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())

        print(f"✅ [EMAIL SERVICE] Sent confirmation email to {to_email} for {product_name}")
        return True
    except Exception as exc:
        print(f"❌ [EMAIL SERVICE ERROR] Failed to send email to {to_email}: {exc}")
        return False
