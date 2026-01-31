from google import genai
import time
import json


import os
from dotenv import load_dotenv




### currently designed as one email at a time
def reading_email(email_input):
    load_dotenv()  # reads .env
    #hidden api
    api_key = os.getenv("google_api")
    client = genai.Client(api_key=api_key)
    ##starting timer
    start_time = time.time()
    ##generating response
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents= "read only the from,subject and snippet field and check if its a spam/newsletter and only return true or false and nothing else." + email_input)  ##example id
    

    #filtering reponse to remove useless html parts
    text = response.candidates[0].content.parts[0].text
    print(text)
    
    end = time.time()

    print("this took ", end - start_time)

    

##calling function
reading_email(d)
