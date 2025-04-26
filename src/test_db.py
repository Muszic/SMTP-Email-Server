#!/usr/bin/env python3
import os
from email_db import EmailDatabase
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

def test_database():
    """Test the email database functionality"""
    print("Testing email database...")
    
    # Initialize the database
    db = EmailDatabase()
    
    # Create test directory
    os.makedirs("database", exist_ok=True)
    
    # Create a test email
    msg = MIMEMultipart()
    msg["From"] = "sender@example.com"
    msg["To"] = "test@example.com"
    msg["Subject"] = "Test Email for Database"
    msg["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    # Add body
    body = "This is a test email to verify database functionality."
    msg.attach(MIMEText(body, "plain"))
    
    # Store the email
    message_data = msg.as_bytes()
    email_id = db.store_email("test@example.com", message_data)
    
    if not email_id:
        print("Error: Failed to store email in database")
        return False
    
    print(f"Email stored with ID: {email_id}")
    
    # Test getting mailbox
    print("\nTesting mailbox retrieval...")
    emails = db.get_mailbox("test@example.com")
    
    if not emails:
        print("Error: No emails found in mailbox")
        return False
    
    print(f"Found {len(emails)} emails in mailbox")
    
    # Test getting specific email
    print("\nTesting email retrieval...")
    mail_data = db.get_email(email_id)
    
    if not mail_data:
        print("Error: Failed to retrieve email")
        return False
    
    print(f"Retrieved email with subject: {mail_data['subject']}")
    
    # Test marking as read
    print("\nTesting marking email as read...")
    if not db.mark_as_read(email_id):
        print("Error: Failed to mark email as read")
        return False
    
    # Verify read status
    mail_data = db.get_email(email_id)
    if not mail_data['is_read']:
        print("Error: Email not marked as read")
        return False
    
    print("Email marked as read successfully")
    
    # Test search
    print("\nTesting email search...")
    search_results = db.search_emails("test@example.com", "test")
    
    if not search_results:
        print("Error: No search results found")
        return False
    
    print(f"Found {len(search_results)} emails matching 'test'")
    
    # Test deletion
    print("\nTesting email deletion...")
    if not db.delete_email(email_id):
        print("Error: Failed to delete email")
        return False
    
    # Verify deletion
    mail_data = db.get_email(email_id)
    if mail_data:
        print("Error: Email not deleted")
        return False
    
    print("Email deleted successfully")
    
    print("\nAll tests passed successfully!")
    return True

if __name__ == "__main__":
    test_database() 