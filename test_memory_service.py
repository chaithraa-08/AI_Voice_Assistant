from memory.memory_service import MemoryService

memory = MemoryService()

print(memory.process("My name is Chaithra"))
print(memory.process("I study at IIITDM Jabalpur"))
print(memory.process("Remember that my project demo is on Friday"))

print()

print(memory.process("What is my name?"))
print(memory.process("Where do I study?"))
print(memory.process("Show my memories"))