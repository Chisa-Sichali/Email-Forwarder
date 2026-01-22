import re
import os
import email
import imaplib
import requests
from dotenv import load_dotenv
from src.helpers.remove_digital_signatures import remove_digital_signatures

load_dotenv()

imap_host = os.getenv('EMAIL_HOST')
username = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASSWORD')
next_api = os.getenv('NEXT_API_ROUTE')

def fetch_and_forward_emails():
    print("Connecting to IMAP server:", imap_host)
    try:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(username, password)
        print("Logged in as:", username)
    except Exception as e:
        print("Failed to connect/login to IMAP:", e)
        return

    mail.select("inbox")
    print("Selected INBOX")

    # Search for unseen emails
    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        print("IMAP search failed:", status)
        return

    email_ids = messages[0].split()[::-1]
    print(f"Found {len(email_ids)} new email(s)")

    for eid in email_ids:
        print("\nProcessing email UID:", eid.decode())
        try:
            _, msg_data = mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = msg["From"]
            subject = msg["Subject"]
            print("From:", sender)
            print("Subject:", subject)

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            body = remove_digital_signatures(body)

            print("Body preview:", body[:100])  # first 100 chars

            payload = {
                "FromName": sender,
                "From": sender,
                "To": username,
                "Subject": subject,
                "TextBody": body,
                "HtmlBody": "",
                "Date": "",
                "MessageID": "",
                "Tag": "",
                "Headers": [],
            }

            # Send to Next.js API
            try:
                response = requests.post(next_api, json=payload)
                print("Forwarded to Next.js API:", next_api)
                print("Response:", response.status_code, response.text)
            except Exception as e:
                print("Failed to send to Next.js API:", e)

            # Mark as read
            mail.store(eid, "+FLAGS", "\\Seen")
            print("Marked email as read")

        except Exception as e:
            print("Failed to process email UID:", eid.decode(), e)

    mail.logout()
    print("Logged out from IMAP")

if __name__ == "__main__":
    fetch_and_forward_emails()
