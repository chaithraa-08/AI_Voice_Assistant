import sqlite3
from memory.memory_extractor import MemoryExtractor
from memory.memory_retriever import MemoryRetriever


class MemoryService:

    def __init__(self):
        self.conn = sqlite3.connect("database/assistant.db")
        self.cursor = self.conn.cursor()

        self.extractor = MemoryExtractor()
        self.retriever = MemoryRetriever()

    def save_memory(self, user, assistant):
        self.cursor.execute(
            """
            INSERT INTO conversations(user, assistant)
            VALUES (?, ?)
            """,
            (user, assistant)
        )
        self.conn.commit()

        print("✅ Memory Saved")
        print("User:", user)
        print("Assistant:", assistant)

    def get_recent_memory(self, limit=5):
        self.cursor.execute(
            """
            SELECT user, assistant
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return self.cursor.fetchall()

    def process(self, user_query):
        text = user_query.lower().strip()

        forget_patterns = {
            "forget my name": "name",
            "forget my favourite course": "favourite_course",
            "forget my favorite course": "favourite_course",
            "forget my hobby": "hobby",
            "forget my goal": "goal",
            "forget my project": "project",
            "forget where i am from": "city"
        }

        for sentence, key in forget_patterns.items():

            if sentence in text:

                self.delete_memory(key)

                return f"Okay! I forgot your {key.replace('_', ' ')}."

        # ------------- SAVE MEMEORIES ----------------

        memory = self.extractor.extract(user_query)

        print("Extracted Memory:", memory)

        if memory.get("save"):

            self.save_user_memory(
                memory["key"],
                memory["value"]
            )

            return f"I'll remember that your {memory['key'].replace('_',' ')} is {memory['value']}."
        # ---------- RETRIEVE MEMORIES ----------
        memory = self.retriever.retrieve(user_query)

        print("Retrieved Memory:", memory)

        key = memory.get("key")

        if key:

            value = self.get_memory(key)

            if value:
                return f"Your {key.replace('_',' ')} is {value}."

            return f"I don't know your {key.replace('_',' ')} yet."

    def clear_user_memories(self):

        self.cursor.execute("DELETE FROM memories")

        self.conn.commit()

        print("🗑️ All memories deleted.")

    def clear_memory(self):
        self.cursor.execute("DELETE FROM conversations")
        self.conn.commit()

    def save_user_memory(self, key, value):

        self.cursor.execute("""
        INSERT INTO memories(memory_key, memory_value)
        VALUES(?, ?)
        ON CONFLICT(memory_key)
        DO UPDATE SET memory_value=excluded.memory_value
        """, (key, value))

        self.conn.commit()

        print(f"✅ Saved Memory: {key} -> {value}")

    def get_memory(self, key):

        self.cursor.execute("""
        SELECT memory_value
        FROM memories
        WHERE memory_key=?
        """, (key,))

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None
    
    def delete_memory(self, key):

        self.cursor.execute("""
        DELETE FROM memories
        WHERE memory_key = ?
        """, (key,))

        self.conn.commit()

        print(f"🗑️ Deleted Memory: {key}")