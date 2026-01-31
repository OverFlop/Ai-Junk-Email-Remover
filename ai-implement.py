from google import genai
import time
import json

with open('mockEmails.json') as f:
    d = str(json.load(f))

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env

#hidden api
api_key = os.getenv("google_api")


### currently designed as one email at a time
def reading_email(email_input):
    client = genai.Client(api_key=api_key)
    ##starting timer
    start_time = time.time()
    ##generating response
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents= "read this email and rank it where its spam or a newsletter reply with just (yes this is a newsletter) or (no it is not) and reply with the email sent with" + email_input)  ##example id

    #filtering reponse to remove useless html parts
    text = response.candidates[0].content.parts[0].text
    print(text)
    end = time.time()

    print("this took ", end - start_time)

    

##calling function
reading_email(d)
