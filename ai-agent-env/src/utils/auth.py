import os
import requests
from urllib.parse import urlencode
from src.utils.helpers import log_message

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# LinkedIn OAuth credentials
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000")

# LinkedIn API endpoints
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

def get_auth_url():
    """
    Generate the LinkedIn OAuth authorization URL.
    """
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "profile w_member_social",
        "state": secrets.token_urlsafe(16),  # Random state for CSRF protection
    }
    auth_url = requests.Request("GET", AUTH_URL, params=params).prepare().url
    return auth_url

def get_access_token(code):
    """
    Exchange the authorization code for an access token.
    """
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get access token: {response.json()}")

def refresh_access_token(refresh_token):
    """
    Refresh the access token using the refresh token.
    """
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to refresh access token: {response.json()}")