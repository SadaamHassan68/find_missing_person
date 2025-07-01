#!/usr/bin/env python3
"""
Admin Setup Script for Missing Person Finder System

This script provides an easy-to-use menu-driven interface for setting up
and managing admin users in the Missing Person Finder System.

Usage:
    python setup_admin.py
"""

import os
import sys
import subprocess
from create_admin_simple import (
    create_admin_user, promote_user_to_admin, 
    list_admin_users, list_all_users,
    validate_email, validate_password
)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header"""
    print("🔧 Missing Person Finder System - Admin Setup")
    print("=" * 50)

def print_menu():
    """Print the main menu"""
    print("\n📋 Available Options:")
    print("1. Create New Admin User")
    print("2. Promote Existing User to Admin")
    print("3. List All Admin Users")
    print("4. List All Users")
    print("5. Generate Admin Registration Token")
    print("6. Exit")
    print("-" * 30)

def create_admin_interactive():
    """Interactive admin creation"""
    clear_screen()
    print_header()
    print("🔧 Creating New Admin User")
    print("=" * 30)
    
    # Get username
    while True:
        username = input("\nEnter username: ").strip()
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
        password = input("Enter password: ")
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                confirm_password = input("Confirm password: ")
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
        success = create_admin_user(username, email, password)
        if success:
            input("\n✅ Admin user created successfully! Press Enter to continue...")
        else:
            input("\n❌ Failed to create admin user. Press Enter to continue...")
    else:
        print("❌ Admin creation cancelled")
        input("Press Enter to continue...")

def promote_user_interactive():
    """Interactive user promotion"""
    clear_screen()
    print_header()
    print("🔧 Promote User to Admin")
    print("=" * 30)
    
    # First, show all users
    print("\n📋 Current Users:")
    print("-" * 80)
    print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Role':<10}")
    print("-" * 80)
    
    try:
        import sqlite3
        conn = sqlite3.connect('missing_persons.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email, role FROM user ORDER BY id")
        users = cursor.fetchall()
        
        for user in users:
            role_display = "👑 ADMIN" if user['role'] == 'admin' else "👤 USER"
            print(f"{user['id']:<5} {user['username']:<20} {user['email']:<30} {role_display:<10}")
        
        conn.close()
        
        # Get user ID to promote
        while True:
            try:
                user_id = input("\nEnter User ID to promote to admin: ").strip()
                if user_id:
                    user_id = int(user_id)
                    break
                else:
                    print("❌ User ID cannot be empty")
            except ValueError:
                print("❌ Please enter a valid number")
        
        success = promote_user_to_admin(user_id)
        if success:
            input("\n✅ User promoted successfully! Press Enter to continue...")
        else:
            input("\n❌ Failed to promote user. Press Enter to continue...")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("Press Enter to continue...")

def list_admin_users_interactive():
    """Interactive admin users listing"""
    clear_screen()
    print_header()
    print("📋 Admin Users")
    print("=" * 30)
    
    list_admin_users()
    input("\nPress Enter to continue...")

def list_all_users_interactive():
    """Interactive all users listing"""
    clear_screen()
    print_header()
    print("📋 All Users")
    print("=" * 30)
    
    list_all_users()
    input("\nPress Enter to continue...")

def generate_token_interactive():
    """Interactive token generation"""
    clear_screen()
    print_header()
    print("🔑 Generate Admin Registration Token")
    print("=" * 40)
    
    try:
        import secrets
        token = secrets.token_urlsafe(32)
        
        print(f"\nGenerated Token: {token}")
        print("\n📝 Usage Instructions:")
        print("1. Copy the token above")
        print("2. Visit: http://localhost:5000/register-admin/<token>")
        print("3. Replace <token> with the generated token")
        print("4. Fill out the admin registration form")
        print("\n⚠️  Security Notes:")
        print("- Keep this token secure and private")
        print("- The token is valid for the current session only")
        print("- Generate a new token for each admin registration")
        print("- The token will change when the application restarts")
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"❌ Error generating token: {str(e)}")
        input("Press Enter to continue...")

def main():
    """Main function"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                create_admin_interactive()
            elif choice == '2':
                promote_user_interactive()
            elif choice == '3':
                list_admin_users_interactive()
            elif choice == '4':
                list_all_users_interactive()
            elif choice == '5':
                generate_token_interactive()
            elif choice == '6':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1-6.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    # Check if database exists
    if not os.path.exists('missing_persons.db'):
        print("❌ Error: Database file 'missing_persons.db' not found")
        print("   Please run the application first to initialize the database")
        sys.exit(1)
    
    main() 