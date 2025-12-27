import os, smtplib, socket, re
from email.message import EmailMessage
from time import sleep

def send_email(body:str, subject:str, retries:int, smtp_user:str, retry_delay=3):
    """
    Send an email using SMTP with retries.
    subject: The subject of the email.
    body: The body of the email.
    smtp_user: The recipient email address.
    retries: The number of retry attempts.
    retry_delay: The delay between retries (in seconds), default is 3.
    """
    
    admin_smtp_user = os.getenv("GMAIL_USER")
    admin_smtp_app_pass = os.getenv("GMAIL_APP_PASSWORD")
    admin_smtp_host = os.getenv("SMTP_HOST")
    admin_smtp_port = int(os.getenv("SMTP_PORT"))

    if not admin_smtp_user or not admin_smtp_app_pass:
        raise SystemExit("Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.")
    
    try:
        socket.gethostbyname(admin_smtp_host)
    except Exception as e:
        raise RuntimeError(f"DNS lookup failed for SMTP host '{admin_smtp_host}': {e}") from e

    msg = EmailMessage()
    msg["From"] = admin_smtp_user
    msg["To"] = smtp_user
    msg["Subject"] = subject
    msg.set_content(body)
    
    last_exec = None
    for attempt in (1, retries + 1):
        try:
            with smtplib.SMTP(admin_smtp_host, admin_smtp_port, timeout=20) as smtp:
                smtp.ehlo()
                if admin_smtp_port == 587:                    
                    smtp.starttls()
                    smtp.ehlo()
                smtp.login(admin_smtp_user, admin_smtp_app_pass)
                smtp.send_message(msg)
                
            #print("Email sent")
            return True
        except Exception as exc:
            last_exec = exc
            #print(f"send_email: attempt {attempt} failed: {exc}")
            if attempt < retries:
                sleep(retry_delay)
    
    #All retries failed
    raise last_exec