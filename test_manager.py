from agents.manager import Manager

manager = Manager()

user_query = input("You: ")

response = manager.process(user_query)

print("\nAssistant:\n")
print(response["response"])