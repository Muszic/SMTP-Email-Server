#!/usr/bin/env python3
import asyncore
import smtpd
import os
import datetime
import email
import uuid
from email.parser import Parser
from email.policy import default
import logging
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='logs/smtp_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('smtp_server')

class MailboxManager:
    """Manages mailboxes for users and email storage"""
    def __init__(self, mailbox_dir='mailboxes'):
        self.mailbox_dir = mailbox_dir
        os.makedirs(self.mailbox_dir, exist_ok=True)
    
    def get_user_mailbox_path(self, user_email):
        """Get path to a user's mailbox directory"""
        # Sanitize email address for filename
        user = user_email.replace('@', '_at_').replace('.', '_dot_')
        user_dir = os.path.join(self.mailbox_dir, user)
        os.makedirs(user_dir, exist_ok=True)
        return user_dir
    
    def store_email(self, recipient, message_data):
        """Store an email in a recipient's mailbox"""
        mailbox_path = self.get_user_mailbox_path(recipient)
        message_id = str(uuid.uuid4())
        
        # Store the email with a unique ID and timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{message_id}.eml"
        
        with open(os.path.join(mailbox_path, filename), 'wb') as f:
            f.write(message_data)
        
        logger.info(f"Stored email for {recipient} with ID {message_id}")
        return message_id

class CustomSMTPServer(smtpd.SMTPServer):
    """Custom SMTP Server that handles email receiving and processing"""
    def __init__(self, localaddr, remoteaddr):
        super().__init__(localaddr, remoteaddr)
        self.mailbox_manager = MailboxManager()
        logger.info(f"SMTP Server started on {localaddr[0]}:{localaddr[1]}")
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        """Process incoming messages"""
        logger.info(f"Receiving message from: {mailfrom} to: {rcpttos}")
        
        try:
            # Parse the email message
            message = email.message_from_bytes(data, policy=default)
            subject = message.get('Subject', 'No Subject')
            
            logger.info(f"Message subject: {subject}")
            
            # Store message for each recipient
            for recipient in rcpttos:
                self.mailbox_manager.store_email(recipient, data)
                
            # Log message details
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "from": mailfrom,
                "to": rcpttos,
                "subject": subject,
                "size": len(data),
                "peer": f"{peer[0]}:{peer[1]}"
            }
            
            with open('logs/message_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
            return "250 Message accepted for delivery"
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "451 Error in processing"

def main():
    """Main function to start the SMTP server"""
    # Create directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('mailboxes', exist_ok=True)
    
    # Get configuration
    host = os.getenv('SMTP_HOST', '127.0.0.1')
    port = int(os.getenv('SMTP_PORT', 1025))
    
    logger.info(f"Starting SMTP server on {host}:{port}")
    server = CustomSMTPServer((host, port), None)
    
    try:
        print(f"SMTP Server running on {host}:{port}")
        print("Press Ctrl+C to stop")
        asyncore.loop()
    except KeyboardInterrupt:
        logger.info("SMTP Server shutting down")
        print("SMTP Server shutting down")

if __name__ == "__main__":
    main() 