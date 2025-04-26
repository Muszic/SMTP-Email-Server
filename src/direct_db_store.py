#!/usr/bin/env python3
import os
from email_db import EmailDatabase

def store_test_email():
    """Store the test email directly in the database"""
    print("Storing test email directly in the database...")
    
    # Initialize the database
    db = EmailDatabase()
    
    # Path to the test email
    email_path = "mailboxes/test_at_example_dot_com/20250426105459_migration_test.eml"
    
    if not os.path.exists(email_path):
        print(f"Error: Test email file not found at {email_path}")
        return
    
    # Read the email file
    with open(email_path, 'rb') as f:
        message_data = f.read()
    
    # Store in database
    email_id = db.store_email("test@example.com", message_data)
    
    if email_id:
        print(f"Email stored successfully with ID: {email_id}")
    else:
        print("Failed to store email in database")
    
    # Check if it's now in the database
    emails = db.get_mailbox("test@example.com")
    print(f"Found {len(emails)} emails for test@example.com in the database")

if __name__ == "__main__":
    store_test_email() 