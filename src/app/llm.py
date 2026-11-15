
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


def generate_answer(message: str, system_prompt: str = "You are a helpful assistant.") -> str:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
