from flask import Flask
import json

# Gets the mock emails in json and converts them to string to return for the AI to read
@app.get("/api/mock-emails")
def mockEmails():
    with open('mockEmails.json') as f:
        mockEmails = json.load(f)

    return mockEmails

