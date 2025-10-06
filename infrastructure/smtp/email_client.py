import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()


class EmailClient:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", 465))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_from = os.getenv("SMTP_FROM")

    def send_email(
            self,
            to: str | List[str],
            subject: str,
            html_content: str,
            text_content: Optional[str] = None
    ) -> bool:
        recipients = [to] if isinstance(to, str) else to

        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.smtp_from
            message["To"] = ", ".join(recipients)

            if text_content:
                text_part = MIMEText(text_content, "plain", "utf-8")
                message.attach(text_part)

            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)

            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_from, recipients, message.as_string())

            return True

        except Exception as e:
            print(f"Error sending email: {e}")

            return False