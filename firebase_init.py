import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import pyrebase
from firebase_config import (
    FIREBASE_API_KEY, FIREBASE_AUTH_DOMAIN, FIREBASE_PROJECT_ID,
    FIREBASE_STORAGE_BUCKET, FIREBASE_APP_ID
)

# Create a temporary service account file for Firebase Admin SDK
service_account = {
    "type": "service_account",
    "project_id": FIREBASE_PROJECT_ID,
    "private_key_id": "temporary_key_id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7VJTUt9Us8cKj\nMzEfYyjiWA4R4/M2bS1GB4t7NXp98C3SC6dVMvDuictGeurT8jNbvJZHtCSuYEvu\nNMoSfm76oqFvAp8Gy0iz5sxjZmSnXyCdPEovGhLa0VzMaQ8s+CLOyS56YyCFGeJZ\n-----END PRIVATE KEY-----\n",
    "client_email": f"firebase-adminsdk@{FIREBASE_PROJECT_ID}.iam.gserviceaccount.com",
    "client_id": "temporary_client_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk%40{FIREBASE_PROJECT_ID}.iam.gserviceaccount.com"
}

service_account_path = 'service-account.json'
with open(service_account_path, 'w') as f:
    json.dump(service_account, f)

# Initialize Firebase Admin SDK with the service account
try:
    # First try with service account file
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred, {
        'projectId': FIREBASE_PROJECT_ID,
        'storageBucket': FIREBASE_STORAGE_BUCKET
    })
except:
    # If that fails, initialize with just the project ID (for development)
    firebase_admin.initialize_app(options={
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