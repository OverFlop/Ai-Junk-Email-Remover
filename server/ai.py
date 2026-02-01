import asyncio
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv


async def reading_email(address, subject, snippet) -> bool:
    load_dotenv()
    api = os.getenv("ROUTERAPI")

    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api
    )

    try:
        completion = await asyncio.wait_for(client.chat.completions.create(
            model="openai/gpt-5.2",
            messages=[
                {
                    "role": "user",
                    "content": f"read the from address {address} subject {subject}, snippet {snippet} from the email and determine whether it is span/newsletter return true or false only "
                }
            ]
        ), timeout=5.0)

        text = completion.choices[0].message.content.strip().lower()
        print(text)
        return text == "true"
    except:
        return False 
