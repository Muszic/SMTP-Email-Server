#!/usr/bin/env python3
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import datetime

# Load environment variables
load_dotenv()

def send_test_email():
    """Send a test email from Alice to Bob"""
    # Email details
    sender = "alice@example.com"
    recipient = "bob@example.com"
    subject = "Test Email from Alice to Bob"
    body = """
    Hello Bob,
    
    This is a test email sent from the user authentication mail client.
    I hope you're doing well!
    
    Best regards,
    Alice
    """
    
    # SMTP server settings
    smtp_host = os.getenv("SMTP_HOST", "127.0.0.1")
    smtp_port = int(os.getenv("SMTP_PORT", "1025"))
    
    # Create the email
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    
    # Add the current date in RFC 2822 format
    message["Date"] = formatdate(localtime=True)
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            print(f"Connected to SMTP server at {smtp_host}:{smtp_port}")
            
            # Send the email
            server.sendmail(sender, recipient, message.as_string())
            print(f"Email sent successfully from {sender} to {recipient}")
            print(f"Date: {message['Date']}")
            
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_test_email() 