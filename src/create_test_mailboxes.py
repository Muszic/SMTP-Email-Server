#!/usr/bin/env python3
import os
import argparse

def create_test_mailboxes(mailbox_dir="mailboxes", users=None):
    """Create test mailboxes for SMTP server testing"""
    if users is None:
        users = [
            "user1@example.com",
            "user2@example.com", 
            "admin@example.com",
            "test@localhost"
        ]
    
    # Create the mailbox directory if it doesn't exist
    os.makedirs(mailbox_dir, exist_ok=True)
    
    # Create a mailbox for each user
    for user in users:
        # Sanitize the email address for use as a directory name
        user_dir = user.replace('@', '_at_').replace('.', '_dot_')
        user_path = os.path.join(mailbox_dir, user_dir)
        
        # Create the user's mailbox directory
        os.makedirs(user_path, exist_ok=True)
        
        print(f"Created mailbox for {user} at {user_path}")

def main():
    """Main function to create test mailboxes"""
    parser = argparse.ArgumentParser(description="Create test mailboxes for SMTP server")
    parser.add_argument("--mailbox-dir", default="mailboxes", help="Directory for mailboxes")
    parser.add_argument("--users", nargs='+', help="List of email addresses to create mailboxes for")
    
    args = parser.parse_args()
    
    create_test_mailboxes(args.mailbox_dir, args.users)
    
    print("\nTest mailboxes created successfully.")
    print("You can now use these addresses to send and receive emails with the SMTP server.")

if __name__ == "__main__":
    main() 