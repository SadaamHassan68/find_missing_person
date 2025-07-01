# Admin User Management Guide

This guide explains how to create and manage admin users for the Missing Person Finder System.

## Overview

The system supports two types of users:
- **Regular Users**: Can register missing person cases and use face scanning
- **Admin Users**: Have full system access including user management, case management, and system administration

## Methods to Create Admin Users

### Method 1: Command Line Script (Recommended)

The `create_admin.py` script provides a secure and flexible way to create admin users.

#### Interactive Creation
```bash
python create_admin.py --create
```
This will prompt you for:
- Username (minimum 3 characters)
- Email (valid format required)
- Password (minimum 8 characters, must include uppercase, lowercase, and digit)
- Password confirmation

#### Command Line Creation
```bash
python create_admin.py --create --username admin --email admin@example.com --password SecurePass123
```

#### List Admin Users
```bash
python create_admin.py --list
```

#### List All Users
```bash
python create_admin.py --all-users
```

#### Promote Existing User to Admin
```bash
python create_admin.py --promote --user-id 1
```

### Method 2: Web Interface

You can also create admin users through the web interface using a secure token.

#### Step 1: Generate Admin Token
```bash
python generate_admin_token.py
```

#### Step 2: Use the Token
1. Copy the generated token
2. Visit: `http://localhost:5000/register-admin/<token>`
3. Replace `<token>` with the generated token
4. Fill out the admin registration form

**Note**: The token changes each time the application restarts for security.

### Method 3: Direct Database Access

For advanced users, you can directly insert admin users into the database:

```python
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin_user = User(
        username='admin',
        email='admin@example.com',
        password=generate_password_hash('SecurePass123'),
        role='admin'
    )
    db.session.add(admin_user)
    db.session.commit()
```

## Admin User Capabilities

Admin users have access to:

### Dashboard Features
- System overview with statistics
- Recent activity monitoring
- User management
- Case management across all users

### User Management
- View all registered users
- Promote users to admin role
- Delete users
- Monitor user activity

### Case Management
- View all missing person cases
- Update case status (missing/found)
- Delete cases
- Export case data

### System Administration
- Generate reports (Excel/PDF)
- View system logs
- Monitor storage usage
- API request tracking

## Security Considerations

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

### Token Security
- Admin registration tokens are session-specific
- Tokens change on application restart
- Keep tokens private and secure
- Generate new tokens for each admin registration

### Access Control
- Admin routes are protected with `@admin_required` decorator
- Regular users cannot access admin features
- All admin actions are logged for audit purposes

## Troubleshooting

### Common Issues

#### "Database file not found"
```bash
# Run the application first to initialize the database
python app.py
```

#### "User already exists"
- Check if the email or username is already registered
- Use `python create_admin.py --all-users` to see existing users

#### "Invalid email format"
- Ensure email follows standard format (user@domain.com)
- Check for typos in the email address

#### "Password too weak"
- Ensure password meets all requirements
- Use a mix of uppercase, lowercase, and digits

### Getting Help

If you encounter issues:

1. Check the application logs for error messages
2. Verify the database exists and is accessible
3. Ensure all dependencies are installed
4. Check file permissions for the database and data directories

## Best Practices

1. **Use Strong Passwords**: Always use strong, unique passwords for admin accounts
2. **Limit Admin Access**: Only create admin accounts for trusted personnel
3. **Regular Audits**: Periodically review admin user list
4. **Secure Tokens**: Keep admin registration tokens secure
5. **Monitor Activity**: Regularly check admin activity logs
6. **Backup Database**: Keep regular backups of the database

## Script Reference

### create_admin.py Options

| Option | Description |
|--------|-------------|
| `--create` | Create a new admin user |
| `--username` | Specify username for admin |
| `--email` | Specify email for admin |
| `--password` | Specify password for admin |
| `--list` | List all admin users |
| `--all-users` | List all users with roles |
| `--promote` | Promote existing user to admin |
| `--user-id` | User ID to promote (with --promote) |

### Examples

```bash
# Interactive admin creation
python create_admin.py --create

# Create admin with specific credentials
python create_admin.py --create --username superadmin --email admin@company.com --password MySecurePass123

# List all admin users
python create_admin.py --list

# Promote user ID 5 to admin
python create_admin.py --promote --user-id 5

# View all users and their roles
python create_admin.py --all-users
```

## Support

For additional support or questions about admin user management, please refer to the main project documentation or contact the development team. 