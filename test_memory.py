from memory.memory_manager import MemoryManager

# Create an object
memory = MemoryManager()

# Save a memory
memory.save_memory(
    "profile",
    "name",
    "Chaithra"
)

# Retrieve the memory
print(memory.get_memory("name"))