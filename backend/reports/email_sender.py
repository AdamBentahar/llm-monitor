import smtplib
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_digest_email(to_email: str):
    print(f"📧 Sending digest report to {to_email}...")
    
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")
    
    if not smtp_user or not smtp_pass:
        print("❌ SMTP credentials not configured in .env file")
        return False
    
    # Read report
    report_content = ""
    if os.path.exists("reports/digest.md"):
        with open("reports/digest.md", "r", encoding="utf-8") as f:
            report_content = f.read()
    
    # Build email
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = "🤖 LLM Monitor — Daily Digest Report"
    
    body = f"""
Hello,

Your daily LLM Monitor digest report is ready!

Preview:
{report_content[:500]}...

Full report attached.

Best regards,
LLM Monitor Bot — EPINEON AI
    """
    msg.attach(MIMEText(body, "plain"))
    
    # Attach report
    if os.path.exists("reports/digest.md"):
        with open("reports/digest.md", "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition",
                "attachment; filename=digest_report.md"
            )
            msg.attach(attachment)
    
    # Send
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {to_email}!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    send_digest_email("adam.bentahar@esith.net")