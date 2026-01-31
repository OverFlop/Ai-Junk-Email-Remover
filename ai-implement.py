from google import genai
import time
import json

with open('mockEmails.json') as f:
    d = str(json.load(f))

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env

api_key = os.getenv("google_api")


def reading_email(email_input):
    client = genai.Client(api_key=api_key)

    start_time = time.time()
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents= "read this email and rank it where its spam or a newsletter reply with just yes or no and reply with the email sent with" + email_input)  ##example id

    text = response.candidates[0].content.parts[0].text
    print(text)
    end = time.time()

    print("this took ", end - start_time)

    


reading_email(d)
