from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
import urllib.parse

app = Flask(__name__)

load_dotenv()

TOKEN_URL = "https://oauth2.googleapis.com/token"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"


@app.post("/api/token")
def get_token():
    data = request.get_json()
    auth_code = data.get("authCode")
    if not auth_code:
        return {"error": "Missing authCode"}, 400
    response = requests.post(TOKEN_URL, data={
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    })
    return response.json()


@app.get("/api/emails")
def get_emails():
    data = request.get_json()
    token = request.authorization.token
    if not token:
        return {"error": "Missing authCode"}, 400
    res = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/messages", params={
        "q": ""
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    res.raise_for_status()
    mails = mails.json()["messages"]
    return mails.json()["messages"]


@app.get("/api/authurl")
def get_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }

    url = AUTH_URL + "?" + urllib.parse.urlencode(params)
    return {"url": url}

@app.get("/api/mock-emails")
def mock_emails():
    return [
        {
            "id": "1",
            "sender": "Medium",
            "subject": "Your weekly digest",
            "unsubscribeUrl": "https://medium.com/unsub"
        }
    ]
