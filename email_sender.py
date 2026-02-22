"""
Email Sender — Sends the digest email via Gmail SMTP.
Uses App Password for authentication (regular password won't work).
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
import config


def send_email(html_content):
    """
    Send the HTML digest email via Gmail SMTP.

    Returns:
        bool: True if email was sent successfully, False otherwise.
    """
    if not config.GMAIL_APP_PASSWORD:
        print("  ✗ GMAIL_APP_PASSWORD not set in .env file!")
        print("    → Generate one at: https://myaccount.google.com/apppasswords")
        return False

    # Build the email
    tz = timezone(timedelta(hours=5))  # PKT
    today = datetime.now(tz).strftime("%b %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{config.EMAIL_SUBJECT_PREFIX} — {today}"
    msg["From"] = config.GMAIL_ADDRESS
    msg["To"] = config.EMAIL_RECIPIENT

    # Plain text fallback
    plain_text = (
        "Your AI Daily Digest is ready!\n"
        "Open this email in an HTML-capable client to see the full digest."
    )
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    # Send via Gmail SMTP
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(config.GMAIL_ADDRESS, config.GMAIL_APP_PASSWORD)
            server.sendmail(
                config.GMAIL_ADDRESS,
                config.EMAIL_RECIPIENT,
                msg.as_string(),
            )

        print(f"  ✓ Email sent to {config.EMAIL_RECIPIENT}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("  ✗ Gmail authentication failed!")
        print("    → Make sure you're using an App Password, not your regular password.")
        print("    → Generate one at: https://myaccount.google.com/apppasswords")
        return False

    except Exception as e:
        print(f"  ✗ Email sending failed: {e}")
        return False
