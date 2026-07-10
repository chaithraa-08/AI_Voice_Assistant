from services.groq_service import GroqService

groq = GroqService()

messages = [
    {
        "role": "user",
        "content": "Say hello in one sentence."
    }
]

response = groq.generate(messages)

print(response)