#!/usr/bin/env python3
import os
import glob
import email
from email.policy import default
from email_db import EmailDatabase

def migrate_emails_to_db():
    """Migrate emails from file-based storage to the database"""
    print("Starting email migration from file system to database...")
    
    # Initialize the database
    db = EmailDatabase()
    
    # Get all mailboxes
    mailboxes_dir = "mailboxes"
    if not os.path.exists(mailboxes_dir):
        print("No mailboxes directory found. Nothing to migrate.")
        return
    
    mailboxes = os.listdir(mailboxes_dir)
    if not mailboxes:
        print("No mailboxes found. Nothing to migrate.")
        return
    
    total_emails = 0
    total_migrated = 0
    
    # Process each mailbox
    for mailbox_dir in mailboxes:
        # Convert mailbox name to email address
        email_address = mailbox_dir.replace('_at_', '@').replace('_dot_', '.')
        mailbox_path = os.path.join(mailboxes_dir, mailbox_dir)
        
        if not os.path.isdir(mailbox_path):
            continue
        
        # Get all .eml files in the mailbox
        email_files = glob.glob(os.path.join(mailbox_path, "*.eml"))
        
        if not email_files:
            print(f"No emails found in mailbox for {email_address}. Skipping.")
            continue
        
        print(f"Migrating {len(email_files)} emails for {email_address}...")
        
        # Process each email file
        for email_file in email_files:
            total_emails += 1
            try:
                with open(email_file, 'rb') as f:
                    # Read the email data
                    message_data = f.read()
                    
                    # Store in database
                    email_id = db.store_email(email_address, message_data)
                    
                    if email_id:
                        total_migrated += 1
                        print(f"Migrated: {os.path.basename(email_file)} -> {email_id}")
                    else:
                        print(f"Failed to migrate: {email_file}")
            except Exception as e:
                print(f"Error migrating {email_file}: {e}")
    
    # Print results
    print("\nMigration completed.")
    print(f"Total emails processed: {total_emails}")
    print(f"Successfully migrated: {total_migrated}")
    print(f"Failed migrations: {total_emails - total_migrated}")
    
    if total_migrated > 0:
        print("\nEmails are now available in both the database and file system.")
        print("You can use the --use-db flag with mail_reader.py to read from the database.")

if __name__ == "__main__":
    migrate_emails_to_db() 