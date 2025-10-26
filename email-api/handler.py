import json
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        receiver_email = body.get('receiver_email')
        subject = body.get('subject')
        body_text = body.get('body_text')

        if not receiver_email or not subject or not body_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        sender_email = os.getenv("SENDER_EMAIL")
        sender_pass = os.getenv("SENDER_PASS")

        msg = MIMEText(body_text)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_pass)
            server.send_message(msg)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully"})
        }

    except smtplib.SMTPAuthenticationError:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Authentication failed"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "details": str(e)})
        }
