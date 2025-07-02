import smtplib
from email.mime.text import MIMEText

def send_verification_email(email: str, token: str):
    verify_link = f"http://127.0.0.1:8000/client/verify-email?token={token}"
    message = MIMEText(f"Click the link to verify your email:\n{verify_link}")
    message["Subject"] = "Verify your email"
    message["From"] = "noreply@example.com"
    message["To"] = email

    # Dummy SMTP server (for testing)
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(message)
