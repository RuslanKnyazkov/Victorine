from scr.config.config import (MAIL, PWS)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
import asyncio


async def send_mail(subject, msg, to = MAIL):
    message = MIMEMultipart()
    message["From"] = MAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(f"<html><body>{msg}</body></html>", "html", "utf-8"))

    smtp_client = SMTP(hostname="smtp.mail.ru", port=465, use_tls=True)
    async with smtp_client:
        await smtp_client.login(MAIL, PWS)
        await smtp_client.send_message(message)

