#!/usr/bin/env python3
from email_db import EmailDatabase

def test_search():
    """Test the email search functionality"""
    print("Testing email search functionality...")
    
    # Initialize the database
    db = EmailDatabase()
    
    # Search for the test email sent from GUI in Bob's mailbox
    search_term = "verify database"
    recipient = "bob@example.com"
    
    results = db.search_emails(recipient, search_term)
    
    print(f'Found {len(results)} emails matching "{search_term}" in {recipient}\'s mailbox')
    
    if results:
        for i, mail in enumerate(results, 1):
            print(f"\nSearch result {i}:")
            print(f"  From: {mail['sender']}")
            print(f"  Subject: {mail['subject']}")
            print(f"  Date: {mail['received_date']}")
            print(f"  ID: {mail['id']}")
            print(f"  Read: {'Yes' if mail['is_read'] else 'No'}")

if __name__ == "__main__":
    test_search() 