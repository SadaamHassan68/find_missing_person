#!/usr/bin/env python3
"""
Generate Admin Registration Token

This script generates a secure admin registration token that can be used
to register admin users through the web interface.

Usage:
    python generate_admin_token.py
"""

import secrets
import sys

def generate_token():
    """Generate a secure admin registration token"""
    return secrets.token_urlsafe(32)

def main():
    print("🔑 Admin Registration Token Generator")
    print("=" * 50)
    
    token = generate_token()
    
    print(f"Generated Token: {token}")
    print()
    print("📝 Usage Instructions:")
    print("1. Copy the token above")
    print("2. Visit: http://localhost:5000/register-admin/<token>")
    print("3. Replace <token> with the generated token")
    print("4. Fill out the admin registration form")
    print()
    print("⚠️  Security Notes:")
    print("- Keep this token secure and private")
    print("- The token is valid for the current session only")
    print("- Generate a new token for each admin registration")
    print("- The token will change when the application restarts")
    
    return token

if __name__ == "__main__":
    main() 