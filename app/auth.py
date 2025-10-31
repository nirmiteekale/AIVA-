import os, requests

FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_API_KEY", "")  # Web API key from Firebase project settings
BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

def _endpoint(path):
    if not FIREBASE_WEB_API_KEY:
        raise RuntimeError("Missing FIREBASE_API_KEY")
    return f"{BASE_URL}:{path}?key={FIREBASE_WEB_API_KEY}"

def signup_email_password(email: str, password: str):
    url = _endpoint("signUp")
    resp = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    return resp.status_code, resp.json()

def signin_email_password(email: str, password: str):
    url = _endpoint("signInWithPassword")
    resp = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    return resp.status_code, resp.json()
