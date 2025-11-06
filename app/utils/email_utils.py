# app/utils/email_utils.py

import smtplib
from email.message import EmailMessage
import logging
from app.config import settings  # Make sure settings has SMTP details

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email using SMTP.

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Check if SMTP settings are configured
    smtp_host = getattr(settings, "smtp_host", None)
    if not smtp_host:
        logger.info("SMTP not configured; skipping sending email.")
        logger.info("Email to %s | Subject: %s | Body: %s", to_email, subject, body)
        return True

    # Prepare the email message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = getattr(settings, "from_email", "no-reply@aidrp.com")
    msg["To"] = to_email
    msg.set_content(body)

    try:
        smtp_port = getattr(settings, "smtp_port", 587)
        smtp_user = getattr(settings, "smtp_user", None)
        smtp_password = getattr(settings, "smtp_password", None)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(msg)

        logger.info("✅ Email sent successfully to %s", to_email)
        return True

    except Exception as e:
        logger.error("❌ Failed to send email to %s: %s", to_email, e)
        return False


# =========================================================
# Test block
# =========================================================
if __name__ == "__main__":
    success = send_email(
        to_email="recipient@example.com",
        subject="Test Email",
        body="Hello! This is a test email from AIDRP platform."
    )
    print("Email sent:", success)
