"""
This script initializes the MySQL database on PythonAnywhere.
Run this script after setting up your database and environment variables.

Usage:
    python initialize_db.py
"""

from app import app, db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting database initialization...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully!")
            
            # You can add initial data here if needed
            # For example, creating an admin user
            from models import User
            from werkzeug.security import generate_password_hash
            
            # Check if admin user already exists
            from sqlalchemy.exc import IntegrityError
            
            try:
                admin_email = app.config.get('ADMIN_EMAIL', 'aadmin@gmail.com')
                admin_user = User.query.filter_by(email=admin_email).first()
                
                if not admin_user:
                    admin = User(
                        username='admin',
                        email=admin_email,
                        password_hash=generate_password_hash(app.config.get('ADMIN_PASSWORD', 'admin')),
                        is_admin=True
                    )
                    db.session.add(admin)
                    db.session.commit()
                    logger.info("Admin user created successfully!")
                else:
                    logger.info("Admin user already exists.")
            
            except IntegrityError:
                db.session.rollback()
                logger.warning("Admin user creation failed - may already exist.")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")