import json
import re

from services.groq_service import GroqService


class PlannerAgent:

    def __init__(self):

        self.groq = GroqService()

        with open(
            "prompts/planner_prompt.txt",
            "r",
            encoding="utf-8"
        ) as file:

            self.system_prompt = file.read()

    def clean_json(self, response):

        response = response.strip()

        # Remove markdown code blocks
        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")

        return response.strip()

    def create_plan(self, user_query,emotion=None):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": f"""
        User Emotion: {emotion if emotion else "unknown"}

        User Query:
        {user_query}
        """
            }
        ]

        response = self.groq.generate(messages)

        print("\nRAW RESPONSE:\n")
        print(response)
        print("\n------------------")

        # Clean the response before parsing
        response = self.clean_json(response)

        try:
            plan = json.loads(response)
            
            return plan

        except Exception as e:

            print("\nPlanner Error:", e)
            print("\nCleaned Response:\n")
            print(response)

            return {
                "steps": [
                    {
                        "agent": "ChatAgent",
                        "tool": "",
                        "action": "respond",
                        "parameters": {
                            "query": user_query
                        }
                    }
                ]
            }