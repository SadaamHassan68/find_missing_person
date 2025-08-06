# Missing Person Finder System - Backend Architecture

## Overview
The backend of the Missing Person Finder System is built using **Python Flask** framework and serves as the data access layer that handles all business logic, data storage, and operational procedures. The backend is invisible to users but powers all functionality including user authentication, face recognition, SMS notifications, and data management.

## Core Backend Components

### 1. **Web Framework & Application Server**
- **Technology**: Flask (Python)
- **Purpose**: Main application server that handles HTTP requests and responses
- **Location**: `app.py` (main application file)

```python
# Main Flask application initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///missing_persons.db'
```

### 2. **Database Layer (Data Access Layer)**
- **Technology**: SQLAlchemy ORM with SQLite database
- **Purpose**: Stores and manages all application data
- **Location**: `models.py`

#### Database Models:
- **User Model**: Handles user authentication and roles
- **Case Model**: Stores missing person case information
- **Photo Model**: Manages face photos and encodings
- **Activity Model**: Tracks system activities and audit logs

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
```

### 3. **Face Recognition Engine**
- **Technology**: OpenCV + face_recognition library
- **Purpose**: Processes face images and performs matching
- **Location**: `utils/face_recognition.py`

#### Key Functions:
- **Face Detection**: Identifies faces in uploaded images
- **Face Encoding**: Converts faces to mathematical representations
- **Face Comparison**: Matches scanned faces against database
- **Accuracy Calculation**: Provides match confidence scores

```python
def compare_faces(img1, img2, tolerance=0.6):
    """
    Compare two images and return match status with accuracy score
    Returns: (is_match, accuracy_score)
    """
```

### 4. **SMS Notification Service**
- **Technology**: Tabaarak ICT SMS API
- **Purpose**: Sends automatic notifications when matches are found
- **Location**: `utils/sms_service.py`

#### Features:
- **Automatic Notifications**: Sends SMS when missing person is found
- **Location Integration**: Includes GPS coordinates and address
- **Somali Language Support**: Messages in Somali language
- **Delivery Tracking**: Monitors SMS delivery status

```python
def send_match_notification(guardian_phone, person_name, location_data, person_data):
    """
    Sends SMS notification with person details and location
    """
```

### 5. **API Layer (RESTful Services)**
- **Technology**: Flask Blueprint routes
- **Purpose**: Provides programmatic access to system functions
- **Location**: `routes/api.py`

#### API Endpoints:
- **Face Matching API**: `/api/scan` - Processes face scans
- **Case Management**: `/api/case/<id>/status` - Updates case status
- **User Management**: `/api/user/<id>/role` - Manages user roles
- **SMS Status**: `/api/sms/status/<message_id>` - Checks SMS delivery

### 6. **Authentication & Security Layer**
- **Technology**: Flask-Login + Werkzeug
- **Purpose**: Manages user sessions and access control
- **Features**:
  - Password hashing and verification
  - Session management
  - Role-based access control (Admin/User)
  - CSRF protection

```python
@admin_required
def admin_only_function():
    # Only accessible by admin users
    pass
```

### 7. **Data Processing & Analytics**
- **Technology**: Pandas + ReportLab
- **Purpose**: Generates reports and analytics
- **Features**:
  - Excel report generation
  - PDF report creation
  - Statistical analysis
  - Data export functionality

### 8. **File Management System**
- **Purpose**: Handles image uploads and storage
- **Storage Locations**:
  - `data/faces/` - Face images
  - `data/encodings/` - Face encoding data
  - `data/uploads/` - General uploads

## Backend Data Flow

### 1. **User Registration Flow**
```
User Input → Password Hashing → Database Storage → Activity Logging
```

### 2. **Case Creation Flow**
```
Form Data → Database Storage → Photo Processing → Face Encoding → Cache Update
```

### 3. **Face Recognition Flow**
```
Image Upload → Face Detection → Encoding Generation → Database Comparison → Match Result
```

### 4. **Match Notification Flow**
```
Match Found → Location Data → SMS Service → Guardian Notification → Activity Logging
```

## Backend Services Architecture

### **Core Services:**
1. **User Service**: Manages user accounts and authentication
2. **Case Service**: Handles missing person case operations
3. **Face Recognition Service**: Processes and matches faces
4. **Notification Service**: Manages SMS communications
5. **Reporting Service**: Generates analytics and reports
6. **File Service**: Manages image uploads and storage

### **Supporting Services:**
1. **Logging Service**: Tracks system activities
2. **Cache Service**: Optimizes face recognition performance
3. **Validation Service**: Ensures data integrity
4. **Export Service**: Handles data export operations

## Database Schema

### **Tables:**
- **users**: User accounts and authentication
- **cases**: Missing person case information
- **photos**: Face images and encodings
- **activities**: System activity audit trail

### **Relationships:**
- User → Cases (One-to-Many)
- Case → Photos (One-to-Many)
- User → Activities (One-to-Many)

## Security Features

### **Authentication:**
- Password hashing using Werkzeug
- Session-based authentication
- CSRF token protection

### **Authorization:**
- Role-based access control
- Admin-only functions
- User data isolation

### **Data Protection:**
- Input validation and sanitization
- SQL injection prevention (SQLAlchemy ORM)
- File upload security

## Performance Optimizations

### **Face Recognition:**
- In-memory face encoding cache
- Batch processing for multiple faces
- Optimized image processing

### **Database:**
- Indexed queries for faster searches
- Efficient relationship loading
- Connection pooling

### **File Storage:**
- Organized directory structure
- Efficient file naming conventions
- Automatic cleanup procedures

## Error Handling & Logging

### **Error Management:**
- Comprehensive exception handling
- User-friendly error messages
- Detailed logging for debugging

### **Activity Tracking:**
- User action logging
- System event recording
- Audit trail maintenance

## API Documentation

### **Authentication Endpoints:**
- `POST /login` - User login
- `POST /register` - User registration
- `POST /register-admin/<token>` - Admin registration

### **Case Management:**
- `GET /cases` - List cases
- `POST /new-case` - Create new case
- `GET /case/<id>` - Get case details
- `PUT /edit-case/<id>` - Update case

### **Face Recognition:**
- `POST /api/scan` - Process face scan
- `GET /scan` - Face scanning interface

### **Administrative:**
- `GET /users` - List users (admin only)
- `POST /api/user/<id>/role` - Update user role
- `DELETE /api/user/<id>` - Delete user
- `GET /reports` - Generate reports

## Deployment Considerations

### **Environment Setup:**
- Python virtual environment
- Required dependencies (requirements.txt)
- Database initialization
- File system permissions

### **Configuration:**
- Environment variables for sensitive data
- Database connection settings
- SMS service credentials
- File storage paths

### **Monitoring:**
- Application logging
- Error tracking
- Performance monitoring
- Database health checks

## Conclusion

The backend of the Missing Person Finder System is a robust, scalable architecture that provides:

- **Secure data management** through SQLAlchemy ORM
- **Advanced face recognition** using OpenCV and face_recognition libraries
- **Real-time notifications** via SMS service integration
- **Comprehensive reporting** with data export capabilities
- **Role-based access control** for administrative functions
- **Audit trail** for all system activities

This backend architecture ensures the system can handle multiple users, process face recognition requests efficiently, and maintain data integrity while providing a secure and reliable foundation for the missing person finding application. 