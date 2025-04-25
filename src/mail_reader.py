#!/usr/bin/env python3
import os
import email
import argparse
import glob
import json
from email.policy import default

class MailReader:
    """Reads and displays emails from mailboxes"""
    def __init__(self, mailbox_dir="mailboxes"):
        self.mailbox_dir = mailbox_dir
    
    def get_user_mailbox_path(self, user_email):
        """Get path to a user's mailbox directory"""
        user = user_email.replace('@', '_at_').replace('.', '_dot_')
        return os.path.join(self.mailbox_dir, user)
    
    def list_mailboxes(self):
        """List all mailboxes"""
        if not os.path.exists(self.mailbox_dir):
            print("No mailboxes found.")
            return []
        
        mailboxes = [d for d in os.listdir(self.mailbox_dir) 
                     if os.path.isdir(os.path.join(self.mailbox_dir, d))]
        
        if not mailboxes:
            print("No mailboxes found.")
        else:
            print("Available mailboxes:")
            for mailbox in mailboxes:
                user = mailbox.replace('_at_', '@').replace('_dot_', '.')
                print(f"- {user}")
        
        return mailboxes
    
    def list_emails(self, user_email):
        """List all emails in a mailbox"""
        mailbox_path = self.get_user_mailbox_path(user_email)
        
        if not os.path.exists(mailbox_path):
            print(f"No mailbox found for {user_email}")
            return []
        
        email_files = sorted(glob.glob(os.path.join(mailbox_path, "*.eml")))
        
        if not email_files:
            print(f"No emails found in mailbox for {user_email}")
        else:
            print(f"Emails for {user_email}:")
            
        emails = []
        for i, email_file in enumerate(email_files, 1):
            with open(email_file, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=default)
                sender = msg.get("From", "Unknown")
                subject = msg.get("Subject", "No Subject")
                date = msg.get("Date", "Unknown Date")
                
                print(f"{i}. From: {sender} | Subject: {subject} | Date: {date}")
                emails.append((i, email_file, msg))
        
        return emails
    
    def read_email(self, email_file):
        """Read and display an email"""
        if not os.path.exists(email_file):
            print(f"Email file not found: {email_file}")
            return None
        
        with open(email_file, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=default)
            
            print("-" * 60)
            print(f"From: {msg.get('From', 'Unknown')}")
            print(f"To: {msg.get('To', 'Unknown')}")
            print(f"Subject: {msg.get('Subject', 'No Subject')}")
            print(f"Date: {msg.get('Date', 'Unknown Date')}")
            print("-" * 60)
            
            # Display message body
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip attachments
                if "attachment" in content_disposition:
                    print(f"[Attachment: {part.get_filename()}]")
                    continue
                
                if content_type == "text/plain":
                    print(part.get_content())
                
            print("-" * 60)
            
            return msg

def main():
    """Main function for the mail reader"""
    parser = argparse.ArgumentParser(description="Read emails from mailboxes")
    parser.add_argument("--list", action="store_true", help="List all mailboxes")
    parser.add_argument("--mailbox", help="Mailbox/user email to read")
    parser.add_argument("--read", type=int, help="Read a specific email by number")
    
    args = parser.parse_args()
    
    reader = MailReader()
    
    if args.list:
        reader.list_mailboxes()
    elif args.mailbox:
        emails = reader.list_emails(args.mailbox)
        if args.read and emails:
            if 1 <= args.read <= len(emails):
                _, email_file, _ = emails[args.read - 1]
                reader.read_email(email_file)
            else:
                print(f"Invalid email number. Choose between 1 and {len(emails)}.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 