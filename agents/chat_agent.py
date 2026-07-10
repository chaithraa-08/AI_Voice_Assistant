from services.groq_service import GroqService


class ChatAgent:

    def __init__(self):
        self.groq = GroqService()

    def execute(self, step):

        query = step["parameters"].get("query", "")

        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": query
            }
        ]

        response = self.groq.generate(messages)

        return {
            "status": "success",
            "result": response
        }