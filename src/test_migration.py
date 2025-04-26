#!/usr/bin/env python3
import os
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from email.utils import formatdate
import smtplib

def send_test_email_for_migration():
    """Send a test email for migration testing"""
    print("Sending a test email for migration testing...")
    
    # Create directories if they don't exist
    os.makedirs("mailboxes/test_at_example_dot_com", exist_ok=True)
    
    # Create a test email
    msg = MIMEMultipart()
    msg["From"] = "migrator@example.com"
    msg["To"] = "test@example.com"
    msg["Subject"] = "Test Email for Migration"
    msg["Date"] = formatdate(localtime=True)
    
    # Add body
    body = "This is a test email to verify the migration functionality."
    msg.attach(MIMEText(body, "plain"))
    
    # Save the email to the file system
    email_path = os.path.join("mailboxes/test_at_example_dot_com", 
                             f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_migration_test.eml")
    
    with open(email_path, 'wb') as f:
        f.write(msg.as_bytes())
    
    print(f"Test email saved to {email_path}")
    print("\nNow run: python3 src/migrate_to_db.py")
    print("Then check: python3 src/mail_reader.py --mailbox test@example.com --use-db")

if __name__ == "__main__":
    send_test_email_for_migration() 