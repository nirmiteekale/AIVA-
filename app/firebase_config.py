import os
import json
from pathlib import Path

# Optional Firebase Admin SDK initialization
# Requires: FIREBASE_CREDENTIALS (path to service account JSON) OR FIREBASE_CREDENTIALS_JSON (inline JSON)
firebase_enabled = False
firebase_db = None

def init_firebase():
    global firebase_enabled, firebase_db
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        cred_path = os.getenv("FIREBASE_CREDENTIALS", "")
        cred_json_inline = os.getenv("FIREBASE_CREDENTIALS_JSON", "")

        if cred_json_inline:
            cred_dict = json.loads(cred_json_inline)
            cred = credentials.Certificate(cred_dict)
        elif cred_path and Path(cred_path).exists():
            cred = credentials.Certificate(cred_path)
        else:
            return False, None

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        firebase_db = firestore.client()
        firebase_enabled = True
        return True, firebase_db
    except Exception as e:
        return False, None
