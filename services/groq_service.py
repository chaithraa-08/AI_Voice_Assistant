import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqService:

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "llama-3.3-70b-versatile"

    def generate(
        self,
        messages,
        temperature=0.3,
        max_tokens=1024
    ):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()