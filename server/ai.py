from openai import OpenAI
import os
from dotenv import load_dotenv


def reading_email(address,subject,snippet) -> bool:
    load_dotenv()
    api = os.getenv("ROUTERAPI")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api
    )

    completion = client.chat.completions.create(
        model="openai/gpt-5.2",
        messages=[
            {
            "role": "user",
            "content": f"read the from address{address} subject {subject}, snippet {snippet} from the email and determine whether it is span/newsletter return true or false only "
            }
    ]
    )

    text = completion.choices[0].message.content.strip().lower()
    print(text)


reading_email("spma@spam","wanna get rich quick","get rich quickly follow this link")