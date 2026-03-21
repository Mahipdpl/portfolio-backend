import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import ContactMessage
from app.schemas.schemas import ContactCreate, ContactOut

router = APIRouter()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")           # your Gmail
SMTP_PASS = os.getenv("SMTP_PASS", "")           # Gmail app password
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "mahipdpl123@gmail.com")


def send_notification_email(msg: ContactMessage):
    """Send email notification when a new contact message arrives."""
    if not SMTP_USER or not SMTP_PASS:
        print("⚠️  SMTP not configured — skipping email notification.")
        return
    try:
        email = MIMEMultipart("alternative")
        email["Subject"] = f"[Portfolio] New message from {msg.name}"
        email["From"] = SMTP_USER
        email["To"] = NOTIFY_EMAIL

        html = f"""
        <div style="font-family:monospace;max-width:600px;margin:auto;padding:24px;background:#f9f9f9;border-radius:8px;">
          <h2 style="color:#f97316;">📬 New Portfolio Contact</h2>
          <table style="width:100%;border-collapse:collapse;">
            <tr><td style="padding:8px;font-weight:bold;">Name</td><td style="padding:8px;">{msg.name}</td></tr>
            <tr><td style="padding:8px;font-weight:bold;">Email</td><td style="padding:8px;">{msg.email}</td></tr>
            <tr><td style="padding:8px;font-weight:bold;">Subject</td><td style="padding:8px;">{msg.subject or "—"}</td></tr>
            <tr><td style="padding:8px;font-weight:bold;vertical-align:top;">Message</td>
                <td style="padding:8px;white-space:pre-wrap;">{msg.message}</td></tr>
          </table>
        </div>
        """
        email.attach(MIMEText(html, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, NOTIFY_EMAIL, email.as_string())
        print(f"✅ Email notification sent for message from {msg.name}")
    except Exception as e:
        print(f"❌ Email send failed: {e}")


@router.post("/", response_model=ContactOut, status_code=201)
def submit_contact(
    payload: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    msg = ContactMessage(**payload.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    background_tasks.add_task(send_notification_email, msg)
    return msg
