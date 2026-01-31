from google import genai

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env

api_key = os.getenv("google_api")


def reading_email():
    client = genai.Client(api_key=api_key)


    response = client.models.generate_content(
        model="gemini-2.5-flash", contents= "read this email and rank it where its spam or a newsletter")  ##example id

    text = response.candidates[0].content.parts[0].text
    print(text)

    


reading_email()
