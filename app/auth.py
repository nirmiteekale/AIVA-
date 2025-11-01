# app/auth.py
import os
import requests
from dotenv import load_dotenv

# Streamlit is optional here, but helps read secrets on cloud
try:
    import streamlit as st
except Exception:
    st = None

load_dotenv()

def _get(name, default=None):
    # Prefer Streamlit secrets (cloud), fallback to env/.env (local)
    if st is not None:
        try:
            if name in st.secrets:
                return st.secrets[name]
        except Exception:
            pass
    return os.getenv(name, default)

API_KEY = _get("FIREBASE_API_KEY")

BASE = "https://identitytoolkit.googleapis.com/v1"

def _post(endpoint: str, payload: dict):
    if not API_KEY:
        # Consumed by UI as a friendly message
        return 400, {"error": {"message": "FIREBASE_API_KEY_MISSING"}}
    url = f"{BASE}/{endpoint}?key={API_KEY}"
    try:
        r = requests.post(url, json=payload, timeout=20)
        return r.status_code, r.json()
    except requests.RequestException as e:
        return 503, {"error": {"message": f"NETWORK_ERROR: {e}"}}

def signup_email_password(email: str, password: str):
    """
    Returns: (status_code, json)
    200-range => success; json contains idToken, email, refreshToken, localId.
    Common errors:
      - EMAIL_EXISTS
      - WEAK_PASSWORD : Password should be at least 6 characters
      - OPERATION_NOT_ALLOWED : Email/Password not enabled in console
    """
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return _post("accounts:signUp", payload)

def signin_email_password(email: str, password: str):
    """
    Returns: (status_code, json)
    Common errors:
      - EMAIL_NOT_FOUND
      - INVALID_PASSWORD
      - USER_DISABLED
    """
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return _post("accounts:signInWithPassword", payload)
