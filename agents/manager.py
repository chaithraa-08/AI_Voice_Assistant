from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.researcher import ResearchAgent
from agents.chat_agent import ChatAgent
from memory.memory_service import MemoryService


class Manager:

    def __init__(self):

        print("******** NEW MANAGER CREATED ********")

        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.researcher = ResearchAgent()
        self.chat = ChatAgent()

        self.memory = MemoryService()

    def process(self, user_query, emotion=None):

        print("=" * 60)
        print("Manager received:", user_query)

        # -------------------------
        # Check Memory
        # -------------------------

        memory_response = self.memory.process(user_query)

        print("Memory response:", memory_response)

        if memory_response:

            print("Returning response from Memory Service")

            return {
                "response": memory_response,
                "plan": [],
                "results": []
            }

        print("No memory match. Going to Planner...")

        # -------------------------
        # Planner
        # -------------------------

        plan = self.planner.create_plan(
            user_query,
            emotion["emotion"] if emotion else None
        )

        if not isinstance(plan, dict):

            return {
                "response": "Planner failed to generate a plan.",
                "plan": [],
                "results": []
            }

        steps = plan.get("steps", [])

        # -------------------------
        # Add Emotion
        # -------------------------

        if emotion:

            for step in steps:

                step.setdefault("parameters", {})
                step["parameters"]["emotion"] = emotion["emotion"]

        results = []
        final_response = ""

        # -------------------------
        # Execute Steps
        # -------------------------

        for step in steps:

            agent = step.get("agent")

            if agent == "ExecutorAgent":

                result = self.executor.execute(step)

            elif agent == "ResearchAgent":

                result = self.researcher.execute(step)

            elif agent == "ChatAgent":

                result = self.chat.execute(step)

            else:

                result = {
                    "status": "info",
                    "message": f"{agent} not implemented."
                }

            print(result)

            results.append(result)

            if isinstance(result, dict):

                if "result" in result:
                    final_response = result["result"]

                elif "message" in result:
                    final_response = result["message"]

        # -------------------------
        # Save Conversation
        # -------------------------

        if final_response:

            self.memory.save_memory(
                user_query,
                final_response
            )

        return {
            "response": final_response,
            "plan": steps,
            "results": results
        }