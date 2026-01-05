import os, smtplib, socket, re
from email.message import EmailMessage
from time import sleep
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def send_email(body:str, subject:str, retries:int, smtp_user:str, retry_delay=3, subtype='plain'):
    """
    Send an email using SMTP with retries.
    subject: The subject of the email.
    body: The body of the email.
    smtp_user: The recipient email address.
    retries: The number of retry attempts.
    retry_delay: The delay between retries (in seconds), default is 3.
    subtype: The content type of the email (plain or html), default is plain.
    """
    
    # admin_smtp_user = os.getenv("GMAIL_USER")
    # admin_smtp_app_pass = os.getenv("GMAIL_APP_PASSWORD")
    # admin_smtp_host = os.getenv("SMTP_HOST")
    # admin_smtp_port = int(os.getenv("SMTP_PORT"))
    
    # Test with mailtrap
    admin_smtp_user = os.getenv("MAILTRAP_USER")
    admin_smtp_app_pass = os.getenv("MAILTRAP_PASSWORD")
    admin_smtp_host = os.getenv("MAILTRAP_HOST")
    admin_smtp_port = int(os.getenv("MAILTRAP_PORT"))

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
    msg.set_content(body, subtype=subtype)
    
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

def send_email_with_template(recipient: str, subject: str, template_name: str, context: dict, retries: int = 3, retry_delay: int = 3):
    """
    Send an email using a Jinja2 template.
    recipient: The recipient email address.
    subject: The subject of the email.
    template_name: The name of the template file (relative to app/templates).
    context: A dictionary of variables to render the template.
    retries: The number of retry attempts.
    retry_delay: The delay between retries (in seconds).
    """
    # Calculate the path to the templates directory
    # app/core/utils/email.py -> app/templates
    template_dir = Path(__file__).resolve().parent.parent.parent / "templates"
    
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template(template_name)
    html_content = template.render(context)
    
    return send_email(html_content, subject, retries, recipient, retry_delay, subtype='html')

