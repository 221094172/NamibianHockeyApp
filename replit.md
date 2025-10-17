# Namibia Hockey Union Management System

## Overview

The Namibia Hockey Union Management System is a Flask-based web application designed to manage hockey teams, players, events, and users for the Namibia Hockey Union. The application provides team registration, player management, event scheduling, and administrative capabilities with both online and offline functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture

**Framework**: Flask web framework with SQLAlchemy ORM for database operations

**Database Strategy**: 
- Primary storage uses SQLite for local development (instance/hockey.db)
- MySQL support configured for production deployment (PythonAnywhere)
- Firebase integration exists but appears incomplete/unused in current implementation
- Database models use Flask-SQLAlchemy with declarative base class

**Authentication & Authorization**:
- Flask-Login for session management and user authentication
- Password hashing using Werkzeug security utilities
- Role-based access control with admin and regular user roles
- User loader function integrates with Flask-Login for session persistence

**Data Models**:
- User: Handles authentication and team management relationships
- Team: Represents hockey teams with division categorization
- Player: Stores player information with many-to-many relationships to teams
- Event: Manages hockey events and tournaments
- Notification: System-wide and team-specific announcements
- Association tables for many-to-many relationships (player_team, team_event)

**File Upload Handling**:
- Image optimization using PIL (Pillow) library
- Secure filename generation with UUID prefixes
- Separate upload folders for logos, player photos, and profile pictures
- Image resizing based on type (logos: 300x300, player photos: 400x500, profile pictures: 200x200)

**Form Validation**:
- Flask-WTF for CSRF protection and form handling
- WTForms validators for input validation
- Custom validators for unique constraints (username, email, team name)
- File upload validation for allowed image extensions

### Frontend Architecture

**Template Engine**: Jinja2 templating with Bootstrap 5 dark theme

**UI Framework**: 
- Bootstrap 5 with Replit's dark theme CSS
- Font Awesome icons for visual elements
- Responsive design with mobile-first approach

**Progressive Web App Features**:
- Service worker implementation for offline functionality
- IndexedDB for client-side data storage
- Cache-first strategy for static assets
- Offline page and connection status indicators

**Client-Side Scripts**:
- Service worker for offline caching and sync
- Offline manager for connection state handling
- Loading animations with hockey-themed visuals
- Form submission state management

### External Dependencies

**Python Packages**:
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: User session management
- Flask-WTF: Form handling and CSRF protection
- Pillow: Image processing and optimization
- email-validator: Email validation
- mysqlclient: MySQL database driver (production)
- gunicorn: WSGI HTTP server (production)

**Frontend Libraries**:
- Bootstrap 5: UI framework
- Font Awesome 6: Icon library
- Firebase SDK: Client-side authentication (partially implemented)

**Third-Party Services**:
- Firebase: Authentication and Firestore database (configured but not fully integrated)
  - Project ID: nhu-connect-47t1m
  - Authentication domain configured
  - Storage bucket configured
- PythonAnywhere: Production hosting platform (MySQL deployment configured)

**Static Asset CDNs**:
- Replit Bootstrap theme CSS
- Font Awesome icon library
- Firebase JavaScript SDK

### Deployment Configurations

**Local Development**:
- SQLite database in instance folder
- Debug mode enabled via environment variable
- Flask development server on port 8080

**Production (PythonAnywhere)**:
- MySQL database configuration
- WSGI application setup
- Environment variable configuration for secrets
- Gunicorn as production WSGI server

**Environment Variables**:
- SECRET_KEY: Flask session encryption
- DATABASE_URL: Database connection string
- ADMIN_EMAIL/PASSWORD/SECRET_CODE: Administrative credentials
- FLASK_DEBUG: Debug mode toggle
- Firebase configuration keys (API key, project ID, app ID)