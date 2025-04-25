#!/usr/bin/env python3
from user_auth import UserAuth

def create_test_users():
    """Create test users for demonstration"""
    auth = UserAuth()
    
    # Register first user
    result1 = auth.register_user('alice', 'alice@example.com', 'password123')
    print('Registered Alice:', result1['success'])
    
    # Register second user
    result2 = auth.register_user('bob', 'bob@example.com', 'password456')
    print('Registered Bob:', result2['success'])

if __name__ == "__main__":
    create_test_users() 