"""
Script to reset and initialize the database for the Namibia Hockey Union app
"""
import os
import sys
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def reset_db():
    """Drop all tables and recreate them"""
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("All tables dropped.")
        
        # Create all tables
        db.create_all()
        print("All tables created.")
        
        # Create admin user
        admin = User(
            username='admin',
            email='aadmin@gmail.com',
            password_hash=generate_password_hash('admin'),
            is_admin=True
        )
        db.session.add(admin)
        
        # Create regular test user
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password'),
            is_admin=False
        )
        db.session.add(user)
        
        db.session.commit()
        print("Initial users created.")
        print("Database reset complete!")

if __name__ == '__main__':
    # Delete the old database file if it exists
    try:
        if os.path.exists('hockey.db'):
            os.remove('hockey.db')
            print("Old database file deleted.")
    except Exception as e:
        print(f"Error deleting database file: {e}")
        sys.exit(1)
    
    # Reset and initialize the database
    reset_db()