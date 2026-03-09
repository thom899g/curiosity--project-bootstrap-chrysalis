# firebase_init.py
# Initialize Firebase Firestore

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def init_firebase():
    """
    Initialize Firebase Admin SDK with the service account key.
    The service account key can be provided as a JSON string in the environment variable
    FIREBASE_CREDENTIALS_JSON, or as a JSON file at the path specified in the environment
    variable GOOGLE_APPLICATION_CREDENTIALS.
    """
    try:
        # Check if Firebase app is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Firebase app is not initialized, so initialize it
        creds = None

        # Option 1: Check for JSON string in environment variable
        if os.getenv('FIREBASE_CREDENTIALS_JSON'):
            creds_json = json.loads(os.getenv('FIREBASE_CREDENTIALS_JSON'))
            creds = credentials.Certificate(creds_json)
        # Option 2: Check for JSON file path in environment variable
        elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            creds = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        else:
            # Try to load from a local file named 'serviceAccountKey.json'
            if os.path.exists('serviceAccountKey.json'):
                creds = credentials.Certificate('serviceAccountKey.json')
            else:
                raise Exception("Firebase credentials not found. Please set FIREBASE_CREDENTIALS_JSON or GOOGLE_APPLICATION_CREDENTIALS environment variable, or place a serviceAccountKey.json file in the project root.")

        firebase_admin.initialize_app(creds)

    # Return Firestore client
    return firestore.client()

# Example usage:
# db = init_firebase()