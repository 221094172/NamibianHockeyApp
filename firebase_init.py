import os
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import pyrebase
from firebase_config import (
    FIREBASE_API_KEY, FIREBASE_AUTH_DOMAIN, FIREBASE_PROJECT_ID,
    FIREBASE_STORAGE_BUCKET, FIREBASE_APP_ID
)

# Initialize Firebase Admin SDK (for server-side operations)
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': FIREBASE_PROJECT_ID,
    'storageBucket': FIREBASE_STORAGE_BUCKET
})

# Get a reference to the Firestore database
db = firestore.client()

# Initialize Pyrebase (for client-side operations like authentication)
firebase_config = {
    "apiKey": FIREBASE_API_KEY,
    "authDomain": FIREBASE_AUTH_DOMAIN,
    "projectId": FIREBASE_PROJECT_ID,
    "storageBucket": FIREBASE_STORAGE_BUCKET,
    "appId": FIREBASE_APP_ID,
    "databaseURL": f"https://{FIREBASE_PROJECT_ID}.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebase_config)
firebase_auth = firebase.auth()
firebase_storage = firebase.storage()

# Helper functions for Firebase operations
def get_user_by_email(email):
    """Get a user by email"""
    try:
        user = auth.get_user_by_email(email)
        return user
    except:
        return None

def create_user(email, password, display_name=None):
    """Create a new user"""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def sign_in_user(email, password):
    """Sign in a user with email and password"""
    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print(f"Error signing in: {e}")
        return None

def upload_file(file_path, storage_path):
    """Upload a file to Firebase Storage"""
    try:
        firebase_storage.child(storage_path).put(file_path)
        return firebase_storage.child(storage_path).get_url(None)
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None