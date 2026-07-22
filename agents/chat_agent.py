from services.groq_service import GroqService


class ChatAgent:

    def __init__(self):
        self.groq = GroqService()

    def execute(self, step):

        query = step["parameters"].get("query", "")
        emotion = step["parameters"].get("emotion", "neutral")

        messages = [
            {
                "role": "system",
                "content": f"""
                You are a helpful AI voice assistant.
                
                The user's detected emotion is: {emotion}.
                
                Adapt your tone naturally.
                
                - If the user is happy, celebrate with them.
                - If the user is sad, be supportive.
                - If the user is anxious or fearful, reassure them.
                - If the user is angry, remain calm and help solve the problem.
                
                Do not explicitly mention the detected emotion unless it is relevant to the conversation.
                """
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