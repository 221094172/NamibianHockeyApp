import os

# Firebase configuration
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "AIzaSyCUowFClJl4w1eMorRvXD3rovIHo6wpv04")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "nhu-connect-47t1m")
FIREBASE_APP_ID = os.environ.get("FIREBASE_APP_ID", "1:408960290922:web:0731f838b599c41e607a13")
FIREBASE_AUTH_DOMAIN = f"{FIREBASE_PROJECT_ID}.firebaseapp.com"
FIREBASE_STORAGE_BUCKET = f"{FIREBASE_PROJECT_ID}.appspot.com"

# Admin configuration
ADMIN_EMAIL = "aadmin@gmail.com"
ADMIN_PASSWORD = "admin"
ADMIN_SECRET_CODE = "admin"  # This is used to verify admin registration

# Flask configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "namibia_hockey_secret_key")
DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"

# Upload directories
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
TEAM_LOGOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'team_logos')
PLAYER_PHOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'player_photos')

# Ensure upload folders exist
for folder in [UPLOAD_FOLDER, TEAM_LOGOS_FOLDER, PLAYER_PHOTOS_FOLDER]:
    os.makedirs(folder, exist_ok=True)