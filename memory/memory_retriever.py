import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class MemoryRetriever:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def retrieve(self, user_message):

        prompt = f"""
You are a memory retrieval classifier.

The user is asking about something they previously told the assistant.

Return ONLY valid JSON.

Examples:

User: What is my name?
Output:
{{"key":"name"}}

User: Do you remember where I am from?
Output:
{{"key":"city"}}

User: Which project am I working on?
Output:
{{"key":"project"}}

User: What do I like doing?
Output:
{{"key":"favourite_activity"}}

User: What is my favourite course?
Output:
{{"key":"favourite_course"}}

If the user is NOT asking about a memory return

{{"key": null}}

User:
{user_message}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content.strip()

        answer = answer.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(answer)
        except:
            return {"key": None}