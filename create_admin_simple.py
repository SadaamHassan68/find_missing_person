#!/usr/bin/env python3
"""
Simple Admin Creation Script for Missing Person Finder System

This script creates admin users directly in the database without importing
the full application (avoiding OpenCV/NumPy dependencies).

Usage:
    python create_admin_simple.py --help
    python create_admin_simple.py --create
    python create_admin_simple.py --create --username admin --email admin@example.com --password secret123
    python create_admin_simple.py --list
    python create_admin_simple.py --promote --user-id 1
"""

import os
import sys
import argparse
import getpass
import re
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"

def get_db_connection():
    """Get database connection"""
    if not os.path.exists('missing_persons.db'):
        raise FileNotFoundError("Database file 'missing_persons.db' not found")
    
    conn = sqlite3.connect('missing_persons.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_admin_user(username, email, password):
    """Create a new admin user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM user WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"❌ Error: User with email '{email}' already exists")
            return False
        
        cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"❌ Error: User with username '{username}' already exists")
            return False
        
        # Create new admin user
        hashed_password = generate_password_hash(password)
        created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            INSERT INTO user (username, email, password, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, hashed_password, 'admin', created_at))
        
        user_id = cursor.lastrowid
        
        # Log the activity
        cursor.execute("""
            INSERT INTO activity (action, details, user_id, timestamp)
            VALUES (?, ?, ?, ?)
        """, ('admin_creation', f'Admin user created: {username} ({email})', user_id, created_at))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"   Email: {email}")
        print(f"   User ID: {user_id}")
        print(f"   Created at: {created_at}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def promote_user_to_admin(user_id):
    """Promote an existing user to admin role"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT username, email, role FROM user WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Error: User with ID {user_id} not found")
            return False
        
        if user['role'] == 'admin':
            print(f"ℹ️  User '{user['username']}' is already an admin")
            return True
        
        # Promote user to admin
        cursor.execute("UPDATE user SET role = ? WHERE id = ?", ('admin', user_id))
        
        # Log the activity
        created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO activity (action, details, user_id, timestamp)
            VALUES (?, ?, ?, ?)
        """, ('role_promotion', f'User promoted to admin: {user["username"]} ({user["email"]})', user_id, created_at))
        
        conn.commit()
        conn.close()
        
        print(f"✅ User '{user['username']}' promoted to admin successfully!")
        print(f"   Email: {user['email']}")
        print(f"   User ID: {user_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error promoting user: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def list_admin_users():
    """List all admin users"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email, created_at FROM user WHERE role = 'admin' ORDER BY id")
        admin_users = cursor.fetchall()
        
        if not admin_users:
            print("ℹ️  No admin users found")
            return
        
        print(f"📋 Found {len(admin_users)} admin user(s):")
        print("-" * 80)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created At':<20}")
        print("-" * 80)
        
        for user in admin_users:
            created_at = user['created_at'][:16] if user['created_at'] else "N/A"
            print(f"{user['id']:<5} {user['username']:<20} {user['email']:<30} {created_at:<20}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error listing admin users: {str(e)}")
        if 'conn' in locals():
            conn.close()

def list_all_users():
    """List all users with their roles"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email, role, created_at FROM user ORDER BY id")
        users = cursor.fetchall()
        
        if not users:
            print("ℹ️  No users found")
            return
        
        print(f"📋 Found {len(users)} user(s):")
        print("-" * 90)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Role':<10} {'Created At':<20}")
        print("-" * 90)
        
        for user in users:
            created_at = user['created_at'][:16] if user['created_at'] else "N/A"
            role_display = "👑 ADMIN" if user['role'] == 'admin' else "👤 USER"
            print(f"{user['id']:<5} {user['username']:<20} {user['email']:<30} {role_display:<10} {created_at:<20}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error listing users: {str(e)}")
        if 'conn' in locals():
            conn.close()

def interactive_create():
    """Interactive admin creation"""
    print("🔧 Interactive Admin User Creation")
    print("=" * 50)
    
    # Get username
    while True:
        username = input("Enter username: ").strip()
        if username:
            if len(username) >= 3:
                break
            else:
                print("❌ Username must be at least 3 characters long")
        else:
            print("❌ Username cannot be empty")
    
    # Get email
    while True:
        email = input("Enter email: ").strip()
        if email:
            if validate_email(email):
                break
            else:
                print("❌ Please enter a valid email address")
        else:
            print("❌ Email cannot be empty")
    
    # Get password
    while True:
        password = getpass.getpass("Enter password: ")
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                confirm_password = getpass.getpass("Confirm password: ")
                if password == confirm_password:
                    break
                else:
                    print("❌ Passwords do not match")
            else:
                print(f"❌ {message}")
        else:
            print("❌ Password cannot be empty")
    
    # Confirm creation
    print(f"\n📝 Admin User Details:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {'*' * len(password)}")
    
    confirm = input("\nCreate this admin user? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        return create_admin_user(username, email, password)
    else:
        print("❌ Admin creation cancelled")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Simple Admin Creation Script for Missing Person Finder System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_admin_simple.py --create                    # Interactive creation
  python create_admin_simple.py --create --username admin --email admin@example.com --password secret123
  python create_admin_simple.py --list                      # List admin users
  python create_admin_simple.py --all-users                 # List all users
  python create_admin_simple.py --promote --user-id 1       # Promote user to admin
        """
    )
    
    parser.add_argument('--create', action='store_true', 
                       help='Create a new admin user')
    parser.add_argument('--username', type=str, 
                       help='Username for the admin user')
    parser.add_argument('--email', type=str, 
                       help='Email for the admin user')
    parser.add_argument('--password', type=str, 
                       help='Password for the admin user')
    parser.add_argument('--list', action='store_true', 
                       help='List all admin users')
    parser.add_argument('--all-users', action='store_true', 
                       help='List all users with their roles')
    parser.add_argument('--promote', action='store_true', 
                       help='Promote an existing user to admin')
    parser.add_argument('--user-id', type=int, 
                       help='User ID to promote to admin')
    
    args = parser.parse_args()
    
    # Check if database exists
    if not os.path.exists('missing_persons.db'):
        print("❌ Error: Database file 'missing_persons.db' not found")
        print("   Please run the application first to initialize the database")
        sys.exit(1)
    
    # Handle different commands
    if args.create:
        if args.username and args.email and args.password:
            # Command line creation
            if not validate_email(args.email):
                print("❌ Error: Invalid email format")
                sys.exit(1)
            
            is_valid, message = validate_password(args.password)
            if not is_valid:
                print(f"❌ Error: {message}")
                sys.exit(1)
            
            success = create_admin_user(args.username, args.email, args.password)
            sys.exit(0 if success else 1)
        else:
            # Interactive creation
            success = interactive_create()
            sys.exit(0 if success else 1)
    
    elif args.list:
        list_admin_users()
    
    elif args.all_users:
        list_all_users()
    
    elif args.promote:
        if not args.user_id:
            print("❌ Error: --user-id is required when using --promote")
            sys.exit(1)
        
        success = promote_user_to_admin(args.user_id)
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 