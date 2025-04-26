#!/usr/bin/env python3
import os
import sys
import argparse
import email
from email.policy import default
import glob
from email_db import EmailDatabase  # Import EmailDatabase

def list_mailboxes():
    """List all available mailboxes"""
    mailboxes_dir = "mailboxes"
    if not os.path.exists(mailboxes_dir):
        print("No mailboxes found.")
        return
    
    mailboxes = os.listdir(mailboxes_dir)
    if not mailboxes:
        print("No mailboxes found.")
        return
    
    print("Available mailboxes:")
    for mailbox in mailboxes:
        # Replace _at_ and _dot_ to display as email
        email_addr = mailbox.replace('_at_', '@').replace('_dot_', '.')
        print(f"  - {email_addr}")

def list_emails_from_files(mailbox):
    """List emails in a mailbox from file system"""
    # Convert email address to mailbox path
    mailbox_path = os.path.join("mailboxes", mailbox.replace('@', '_at_').replace('.', '_dot_'))
    
    if not os.path.exists(mailbox_path):
        print(f"Mailbox for {mailbox} not found.")
        return
    
    emails = glob.glob(os.path.join(mailbox_path, "*.eml"))
    if not emails:
        print(f"No emails found in mailbox for {mailbox}.")
        return
    
    print(f"Emails in mailbox for {mailbox}:")
    for i, email_path in enumerate(sorted(emails, reverse=True), 1):
        with open(email_path, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=default)
            subject = msg.get('Subject', 'No Subject')
            from_addr = msg.get('From', 'Unknown')
            date = msg.get('Date', 'Unknown')
            print(f"  {i}. From: {from_addr}")
            print(f"     Subject: {subject}")
            print(f"     Date: {date}")
            print(f"     ID: {os.path.basename(email_path)}")
            print()

def list_emails_from_db(mailbox):
    """List emails in a mailbox from database"""
    db = EmailDatabase()
    emails = db.get_mailbox(mailbox)
    
    if not emails:
        print(f"No emails found in mailbox for {mailbox}.")
        return
    
    print(f"Emails in mailbox for {mailbox}:")
    for i, mail in enumerate(emails, 1):
        print(f"  {i}. From: {mail['sender']}")
        print(f"     Subject: {mail['subject']}")
        print(f"     Date: {mail['received_date']}")
        print(f"     ID: {mail['id']}")
        print(f"     Read: {'Yes' if mail['is_read'] else 'No'}")
        print()

def read_email_from_files(mailbox, index):
    """Read a specific email from file system"""
    # Convert email address to mailbox path
    mailbox_path = os.path.join("mailboxes", mailbox.replace('@', '_at_').replace('.', '_dot_'))
    
    if not os.path.exists(mailbox_path):
        print(f"Mailbox for {mailbox} not found.")
        return
    
    emails = sorted(glob.glob(os.path.join(mailbox_path, "*.eml")), reverse=True)
    if not emails or index > len(emails):
        print(f"Email {index} not found in mailbox for {mailbox}.")
        return
    
    email_path = emails[index - 1]
    
    with open(email_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=default)
        
        # Print email headers
        print(f"From: {msg.get('From', 'Unknown')}")
        print(f"To: {msg.get('To', 'Unknown')}")
        print(f"Subject: {msg.get('Subject', 'No Subject')}")
        print(f"Date: {msg.get('Date', 'Unknown')}")
        print()
        
        # Print email body
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.get_content_type() == 'text/plain':
                    print(part.get_content())
        else:
            print(msg.get_content())

def read_email_from_db(mailbox, email_id):
    """Read a specific email from database"""
    db = EmailDatabase()
    
    # If email_id is an integer, fetch the corresponding email from the list
    if isinstance(email_id, int):
        emails = db.get_mailbox(mailbox)
        if not emails or email_id > len(emails):
            print(f"Email {email_id} not found in mailbox for {mailbox}.")
            return
        
        email_id = emails[email_id - 1]['id']
    
    # Get the email from the database
    mail_data = db.get_email(email_id)
    
    if not mail_data:
        print(f"Email with ID {email_id} not found.")
        return
    
    # Mark as read
    db.mark_as_read(email_id)
    
    # Print email details
    print(f"From: {mail_data['sender']}")
    print(f"To: {mail_data['recipient']}")
    print(f"Subject: {mail_data['subject']}")
    print(f"Date: {mail_data['received_date']}")
    print()
    
    # Print email body
    print(mail_data['body'])
    
    # Print attachments if any
    if mail_data['attachments']:
        import json
        attachments = json.loads(mail_data['attachments'])
        if attachments:
            print("\nAttachments:")
            for attachment in attachments:
                print(f"  - {attachment}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Mail reader for viewing emails")
    
    parser.add_argument("--list", action="store_true", help="List all mailboxes")
    parser.add_argument("--mailbox", help="Mailbox (email address) to read from")
    parser.add_argument("--read", type=int, help="Read a specific email by index")
    parser.add_argument("--id", help="Read a specific email by ID")
    parser.add_argument("--use-db", action="store_true", help="Use database instead of file system")
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Determine whether to use database or files
    use_db = args.use_db or os.path.exists("database/emails.db")
    
    if args.list:
        list_mailboxes()
    elif args.mailbox:
        if args.read:
            if use_db:
                read_email_from_db(args.mailbox, args.read)
            else:
                read_email_from_files(args.mailbox, args.read)
        elif args.id:
            if use_db:
                read_email_from_db(args.mailbox, args.id)
            else:
                print("Reading by ID is only supported with database storage")
        else:
            if use_db:
                list_emails_from_db(args.mailbox)
            else:
                list_emails_from_files(args.mailbox)
    else:
        print("Please specify a mailbox to read from or use --list to see all mailboxes.")
        sys.exit(1)

if __name__ == "__main__":
    main() 