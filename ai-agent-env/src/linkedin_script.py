import os
import time
import requests
from src.utils.auth import get_access_token, get_profile, refresh_access_token
from src.utils.helpers import log_message, retry_on_failure

# LinkedIn API endpoints
POST_URL = "https://api.linkedin.com/v2/ugcPosts"
LIKE_URL = "https://api.linkedin.com/v2/socialActions/{urn}/likes"

def post_to_linkedin(access_token, content):
    """
    Post content to LinkedIn.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Fetch user profile to get the author URN
    profile = get_profile(access_token)
    author_urn = f"urn:li:person:{profile['id']}"

    # Create the post payload
    post_data = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content,
                },
                "shareMediaCategory": "NONE",
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    # Make the API request
    response = requests.post(POST_URL, headers=headers, json=post_data)
    if response.status_code == 201:
        print("Post published successfully!")
    else:
        print("Failed to publish post:", response.json())

def like_post(access_token, post_urn):
    """
    Like a LinkedIn post.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Make the API request
    response = requests.post(LIKE_URL.format(urn=post_urn), headers=headers)
    if response.status_code == 201:
        print("Post liked successfully!")
    else:
        print("Failed to like post:", response.json())

def automate_linkedin(access_token):
    """
    Automate LinkedIn actions (e.g., posting, liking).
    """
    while True:
        # Post content
        post_to_linkedin(access_token, "Check out Vanguard AI - the future of AI agents! 🚀 #AI #Blockchain #VANGAI")

        # Like a post (example URN)
        like_post(access_token, "urn:li:share:1234567890")

        # Wait for 6 hours before the next action
        time.sleep(6 * 3600)

if __name__ == "__main__":
    # Get the access token (replace with your actual code)
    code = input("Enter the authorization code: ")
    access_token = get_access_token(code)

    # Start LinkedIn automation
    automate_linkedin(access_token)