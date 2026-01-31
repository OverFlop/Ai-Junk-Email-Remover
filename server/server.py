import asyncio

import aiohttp
from flask import Flask, request
from flask_cors import CORS
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
async def get_token():
    data = request.get_json()
    auth_code = data.get("authCode")
    if not auth_code:
        return {"error": "Missing authCode"}, 400
    with aiohttp.ClientSession() as session:
        response = await session.post(TOKEN_URL, data={
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        })
    return response.json()


async def get_email(session: aiohttp.ClientSession, mail_id, token):
    print(f"Fetching mail {mail_id}")
    res = await session.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{mail_id}", params={
        "format": "metadata"
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    print(f"Done fetching mail {mail_id}")
    res.raise_for_status()
    return await res.json()


@app.get("/api/emails")
async def get_emails():
    data = request.get_json()
    token = request.authorization.token
    params = {}
    if request.args.get("maxResults"):
        params["maxResults"] = request.args["maxResults"]
    if request.args.get("pageToken"):
        params["pageToken"] = request.args["pageToken"]
    if not token:
        return {"error": "Missing authCode"}, 400
    async with aiohttp.ClientSession() as session:
        res = await session.get("https://gmail.googleapis.com/gmail/v1/users/me/messages", params=params, headers={
            "Authorization": f"Bearer {token}"
        })
        res.raise_for_status()
        data = await res.json()
        tasks = []
        for mail in data["messages"]:
            tasks.append(get_email(session, mail["id"], token))
        mails = await asyncio.gather(*tasks)
        return {"nextPageToken": data["nextPageToken"], "data": mails}


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
