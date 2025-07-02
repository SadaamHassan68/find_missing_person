# Missing Person Finder System

A web-based application that helps find missing persons using facial recognition technology. The system allows users to register missing person cases and scan faces to find potential matches.

## Features

- User Authentication (Login/Register)
- Admin and User Dashboards
- Missing Person Case Management
- Real-time Face Scanning
- Location Tracking
- SMS Notifications for Matches
- Reporting and Analytics
- Export Data to Excel/PDF

## Technology Stack

- Python 3.x
- Flask Web Framework
- SQLAlchemy ORM
- OpenCV for Face Detection
- Bootstrap 5 for UI
- SQLite Database

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd Missing-Person-Finder-System
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Admin User Management

The system includes comprehensive admin user management tools. Admin users have full system access including user management, case management, and system administration.

### Quick Admin Setup

#### Method 1: Interactive Setup (Recommended)
```bash
python setup_admin.py
```
This provides a menu-driven interface for all admin operations.

#### Method 2: Command Line Script
```bash
# Create admin interactively
python create_admin_simple.py --create

# Create admin with specific credentials
python create_admin_simple.py --create --username admin --email admin@example.com --password SecurePass123

# List all admin users
python create_admin_simple.py --list

# Promote existing user to admin
python create_admin_simple.py --promote --user-id 1
```

#### Method 3: Web Interface
```bash
# Generate admin registration token
python generate_admin_token.py

# Use the token in your browser
# Visit: http://localhost:5000/register-admin/<token>
```

### Admin User Capabilities

- **Dashboard**: System overview with statistics and monitoring
- **User Management**: View, promote, and manage all users
- **Case Management**: Access and manage all missing person cases
- **System Administration**: Generate reports, view logs, monitor usage

For detailed admin management instructions, see [ADMIN_SETUP.md](ADMIN_SETUP.md).

## Project Structure

```
Missing-Person-Finder-System/
├── app.py                    # Main application file
├── models.py                 # Database models
├── create_admin_simple.py    # Admin creation script
├── setup_admin.py           # Interactive admin setup
├── generate_admin_token.py  # Token generation script
├── ADMIN_SETUP.md           # Admin management guide
├── routes/                  # Route handlers
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── data/                    # Data storage
│   ├── faces/              # Stored face images
│   ├── encodings/          # Face encodings
│   └── uploads/            # Temporary uploads
└── utils/                  # Utility functions
```

## Usage

1. Register an account or login
2. For admin access, use the admin registration link with the provided token
3. Add missing person cases with photos and details
4. Use the face scanning feature to find potential matches
5. View and manage cases through the dashboard
6. Generate reports and export data as needed

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please contact [+252613695258]
