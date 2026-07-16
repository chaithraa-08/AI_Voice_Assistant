import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class MemoryExtractor:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def extract(self, user_message):

        prompt = f"""
You are a memory extraction system.

If the user tells a personal fact that should be remembered,
return ONLY valid JSON in this format:

{{
    "save": true,
    "key": "memory_key",
    "value": "memory_value"
}}

Examples:

User: My name is Chaithra
Output:
{{"save": true, "key":"name", "value":"Chaithra"}}

User: I am from Telangana
Output:
{{"save": true, "key":"city", "value":"Telangana"}}

User: My favourite course is DBMS
Output:
{{"save": true, "key":"favourite_course", "value":"DBMS"}}

User: I am working on AI Voice Assistant
Output:
{{"save": true, "key":"project", "value":"AI Voice Assistant"}}

If nothing should be remembered return

{{"save": false}}

User:
{user_message}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content.strip()

        try:
            return json.loads(answer)
        except:
            return {"save": False}