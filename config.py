import os

# Flask configuration
SECRET_KEY = os.environ.get("SESSION_SECRET", "namibia_hockey_secret_key")
DEBUG = True

# Admin configuration
ADMIN_EMAIL = "aadmin@gmai.com"
ADMIN_PASSWORD = "admin"
ADMIN_SECRET_CODE = "admin"  # This is used to verify admin registration