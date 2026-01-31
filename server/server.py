import asyncio
from datetime import datetime

import aiohttp
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import urllib.parse

from server import utils

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

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
    async with aiohttp.ClientSession() as session:
        response = await session.post(TOKEN_URL, data={
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        })
    return await response.json()


async def get_email(session: aiohttp.ClientSession, sem: asyncio.Semaphore, mail_id, token):
    async with sem:
        print(f"Fetching mail {mail_id}")
        res = await session.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{mail_id}", params={
            "format": "metadata"
        }, headers={
            "Authorization": f"Bearer {token}"
        })
    print(f"Done fetching mail {mail_id}")
    res.raise_for_status()
    data = await res.json()
    headers = {header["name"].strip().lower(): header["value"] for header in data["payload"]["headers"]}
    unsubscribe_info = utils.parse_unsubscribe_header(headers["list-unsubscribe"])
    unsubscribe_method = "NOT_POSSIBLE"
    if headers["list-unsubscribe-post"] == "List-Unsubscribe=One-Click" and unsubscribe_info["url"]:
        unsubscribe_method = "POST"
    elif unsubscribe_info["mailto"]:
        unsubscribe_method = "MAILTO"
    elif unsubscribe_info["url"]:
        unsubscribe_method = "MANUAL"
    mail = {
        "id": data["id"],
        "receivedAt": datetime.fromtimestamp(int(data["internalDate"]) / 1000.0),
        "labels": data.get("labelIds", []),
        "snippet": data["snippet"].encode("ascii", "ignore").decode().strip(),
        "from": headers["from"],
        "subject": headers["subject"].encode("ascii", "ignore").decode().strip(),
        "listUnsubscribeUrl": unsubscribe_info["url"],
        "listUnsubscribeAddress": unsubscribe_info["mailto"],
        "unsubscribeMethod": unsubscribe_method,
    }

    return mail

async def unsubscribe_mail(session, sem, id, token, failed: list):
    try:
        mail = await get_email(session, sem, id, token)
        if mail["unsubscribeMethod"] == "NOT_POSSIBLE" or mail["unsubscribeMethod"] == "MANUAL":
            failed.append(id)
            return
        if mail["unsubscribeMethod"] == "POST":
            await unsubscribe_post(session, mail["unsubscribeUrl"])
        elif mail["unsubscribeMethod"] == "MAILTO":
            await unsubscribe_mailto(session, sem, )
    except:
        failed.append(id)


@app.post("/api/unsubscribe")
async def batch_unsubscribe_emails():
    token = request.authorization.token
    body = request.get_json()
    email_ids = body.get("emailIds")
    if not isinstance(email_ids, list):
        return {"error": "invalid payload"}, 400
    sem = asyncio.Semaphore(20)
    failed = []
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(unsubscribe_mail(session, sem, id, token, failed) for id in email_ids))
    return {"failed": failed}


@app.get("/api/emails")
async def get_emails():
    token = request.authorization.token
    params = {}
    if request.args.get("maxResults"):
        params["maxResults"] = request.args["maxResults"]
    if request.args.get("pageToken"):
        params["pageToken"] = request.args["pageToken"]
    if not token:
        return {"error": "Missing authCode"}, 400
    sem = asyncio.Semaphore(20)
    async with aiohttp.ClientSession() as session:
        res = await session.get("https://gmail.googleapis.com/gmail/v1/users/me/messages", params=params, headers={
            "Authorization": f"Bearer {token}"
        })
        res.raise_for_status()
        data = await res.json()
        tasks = []
        for mail in data["messages"]:
            tasks.append(get_email(session, sem, mail["id"], token))
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
    with open('../mockEmails.json') as f:
        mockEmails = json.load(f)

    return mockEmails
