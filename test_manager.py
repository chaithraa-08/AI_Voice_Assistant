from agents.manager import Manager

manager = Manager()

query = input("You: ")

result = manager.process(query)

print("\nAssistant:\n")

for r in result:
    print(r)