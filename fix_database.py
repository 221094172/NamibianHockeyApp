"""
Script to fix database issues by recreating it with the correct schema
"""
import os
import sqlite3
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

# Path to SQLite database
DB_PATH = 'instance/hockey.db'

def ensure_directory_exists():
    """Ensure the instance directory exists"""
    os.makedirs('instance', exist_ok=True)

def drop_database():
    """Drop the database file if it exists"""
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"Removed existing database: {DB_PATH}")
    except Exception as e:
        print(f"Error removing database: {e}")

def create_schema():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Created database schema")
        
        # Create admin user
        admin = User(
            username='admin',
            email='aadmin@gmail.com',
            password_hash=generate_password_hash('admin'),
            is_admin=True
        )
        db.session.add(admin)
        
        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password'),
            is_admin=False
        )
        db.session.add(user)
        
        db.session.commit()
        print("Created initial users")

def main():
    """Main function to fix database"""
    print("Starting database fix...")
    ensure_directory_exists()
    drop_database()
    create_schema()
    print("Database fix completed successfully!")

if __name__ == "__main__":
    main()