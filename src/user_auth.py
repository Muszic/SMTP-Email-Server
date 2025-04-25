#!/usr/bin/env python3
import os
import json
import hashlib
import uuid
from datetime import datetime

class UserAuth:
    """User authentication and management system"""
    
    def __init__(self, users_dir="users"):
        """Initialize user authentication system"""
        self.users_dir = users_dir
        self.users_file = os.path.join(users_dir, "users.json")
        self.current_user = None
        
        # Create users directory if it doesn't exist
        os.makedirs(users_dir, exist_ok=True)
        
        # Create users file if it doesn't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)
    
    def _load_users(self):
        """Load users from the users file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_users(self, users):
        """Save users to the users file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _hash_password(self, password, salt=None):
        """Hash a password with a salt"""
        if salt is None:
            salt = uuid.uuid4().hex
            
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return {'hash': hashed, 'salt': salt}
    
    def _verify_password(self, password, hashed_password):
        """Verify a password against a hashed password"""
        salt = hashed_password['salt']
        return self._hash_password(password, salt)['hash'] == hashed_password['hash']
    
    def register_user(self, username, email, password):
        """Register a new user"""
        # Load existing users
        users = self._load_users()
        
        # Check if the user already exists
        for user in users:
            if user['username'] == username:
                return {'success': False, 'error': 'Username already exists'}
            if user['email'] == email:
                return {'success': False, 'error': 'Email already exists'}
        
        # Hash the password
        password_data = self._hash_password(password)
        
        # Create the new user
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'password': password_data,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        # Add the user
        users.append(new_user)
        
        # Save the users
        self._save_users(users)
        
        # Create mailbox for the user
        self._create_mailbox(email)
        
        return {'success': True, 'user': self._sanitize_user(new_user)}
    
    def login(self, email, password):
        """Log in a user"""
        # Load users
        users = self._load_users()
        
        # Find the user
        for user in users:
            if user['email'] == email:
                # Check the password
                if self._verify_password(password, user['password']):
                    # Update last login
                    user['last_login'] = datetime.now().isoformat()
                    self._save_users(users)
                    
                    # Set current user
                    self.current_user = user
                    
                    return {'success': True, 'user': self._sanitize_user(user)}
                else:
                    return {'success': False, 'error': 'Invalid password'}
        
        return {'success': False, 'error': 'User not found'}
    
    def logout(self):
        """Log out the current user"""
        if self.current_user:
            current_user = self.current_user
            self.current_user = None
            return {'success': True, 'user': self._sanitize_user(current_user)}
        
        return {'success': False, 'error': 'No user is logged in'}
    
    def get_current_user(self):
        """Get the current user"""
        if self.current_user:
            return {'success': True, 'user': self._sanitize_user(self.current_user)}
        
        return {'success': False, 'error': 'No user is logged in'}
    
    def _sanitize_user(self, user):
        """Remove sensitive data from a user object"""
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'last_login': user['last_login']
        }
    
    def _create_mailbox(self, email):
        """Create a mailbox for a user"""
        mailbox_dir = "mailboxes"
        os.makedirs(mailbox_dir, exist_ok=True)
        
        # Sanitize email for directory name
        user_dir = email.replace('@', '_at_').replace('.', '_dot_')
        user_path = os.path.join(mailbox_dir, user_dir)
        
        # Create the user's mailbox directory
        os.makedirs(user_path, exist_ok=True)
        
        return user_path

# Example usage
if __name__ == "__main__":
    auth = UserAuth()
    
    # Register user
    result = auth.register_user("testuser", "test@example.com", "password123")
    print("Register:", result)
    
    # Login user
    result = auth.login("test@example.com", "password123")
    print("Login:", result)
    
    # Get current user
    result = auth.get_current_user()
    print("Current user:", result)
    
    # Logout user
    result = auth.logout()
    print("Logout:", result) 