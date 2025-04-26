#!/usr/bin/env python3
import os
import sqlite3
import datetime
import json
import email
from email.policy import default

class EmailDatabase:
    """Database manager for storing and retrieving emails"""
    
    def __init__(self, db_path="database/emails.db"):
        """Initialize the email database"""
        self.db_dir = os.path.dirname(db_path)
        self.db_path = db_path
        
        # Create database directory if it doesn't exist
        os.makedirs(self.db_dir, exist_ok=True)
        
        # Connect to database and create tables if they don't exist
        self._init_db()
    
    def _init_db(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create emails table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            received_date TIMESTAMP NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            raw_email BLOB,
            attachments TEXT
        )
        ''')
        
        # Create index on recipient for faster mailbox access
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_recipient ON emails (recipient)
        ''')
        
        conn.commit()
        conn.close()
    
    def store_email(self, recipient, message_data):
        """Store an email in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Parse the email message
            message = email.message_from_bytes(message_data, policy=default)
            
            # Extract email parts
            email_id = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{message.get('Message-ID', '')}"
            sender = message.get('From', 'Unknown')
            subject = message.get('Subject', 'No Subject')
            
            # Get the body of the email
            body = ""
            attachments = []
            
            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))
                    
                    # Handle text parts as body
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_content()
                    
                    # Handle attachments (simplified)
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            attachments.append(filename)
            else:
                body = message.get_content()
            
            # Insert the email into the database
            cursor.execute('''
            INSERT INTO emails (id, sender, recipient, subject, body, received_date, is_read, raw_email, attachments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                email_id,
                sender,
                recipient,
                subject,
                body,
                datetime.datetime.now().isoformat(),
                False,
                message_data,
                json.dumps(attachments)
            ))
            
            conn.commit()
            return email_id
            
        except Exception as e:
            # Log the error and rollback
            print(f"Error storing email: {e}")
            conn.rollback()
            return None
            
        finally:
            conn.close()
    
    def get_mailbox(self, email_address, limit=50, offset=0):
        """Get emails for a specific mailbox (recipient)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT id, sender, recipient, subject, received_date, is_read 
            FROM emails 
            WHERE recipient = ? 
            ORDER BY received_date DESC
            LIMIT ? OFFSET ?
            ''', (email_address, limit, offset))
            
            emails = [dict(row) for row in cursor.fetchall()]
            return emails
            
        except Exception as e:
            print(f"Error getting mailbox: {e}")
            return []
            
        finally:
            conn.close()
    
    def get_email(self, email_id):
        """Get a specific email by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT * FROM emails WHERE id = ?
            ''', (email_id,))
            
            email_data = cursor.fetchone()
            if email_data:
                return dict(email_data)
            return None
            
        except Exception as e:
            print(f"Error getting email: {e}")
            return None
            
        finally:
            conn.close()
    
    def mark_as_read(self, email_id):
        """Mark an email as read"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE emails SET is_read = 1 WHERE id = ?
            ''', (email_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error marking email as read: {e}")
            conn.rollback()
            return False
            
        finally:
            conn.close()
    
    def delete_email(self, email_id):
        """Delete an email from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            DELETE FROM emails WHERE id = ?
            ''', (email_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error deleting email: {e}")
            conn.rollback()
            return False
            
        finally:
            conn.close()
    
    def search_emails(self, recipient, query, limit=50, offset=0):
        """Search emails in a mailbox by subject or content"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT id, sender, recipient, subject, received_date, is_read 
            FROM emails 
            WHERE recipient = ? AND (subject LIKE ? OR body LIKE ?) 
            ORDER BY received_date DESC
            LIMIT ? OFFSET ?
            ''', (recipient, f"%{query}%", f"%{query}%", limit, offset))
            
            emails = [dict(row) for row in cursor.fetchall()]
            return emails
            
        except Exception as e:
            print(f"Error searching emails: {e}")
            return []
            
        finally:
            conn.close()

# Example usage
if __name__ == "__main__":
    db = EmailDatabase()
    print("Database initialized") 