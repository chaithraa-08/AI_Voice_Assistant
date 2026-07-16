from memory.memory_service import MemoryService

class MemoryManager:

    def __init__(self):
        self.service = MemoryService()

    def remember(self, user, assistant):
        self.service.save_memory(user, assistant)

    def recall(self):
        return self.service.get_recent_memory()