from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.researcher import ResearchAgent
from agents.chat_agent import ChatAgent


class Manager:

    def __init__(self):

        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.researcher = ResearchAgent()
        self.chat = ChatAgent()

    def process(self, user_query):

        # Get execution plan from planner
        plan = self.planner.create_plan(user_query)

        results = []
        final_response = ""

        # Execute each step
        for step in plan["steps"]:

            if step["agent"] == "ExecutorAgent":

                result = self.executor.execute(step)
                print(result)

            elif step["agent"] == "ResearchAgent":

                result = self.researcher.execute(step)
                print(result)

            elif step["agent"] == "ChatAgent":

                result = self.chat.execute(step)
                print(result)

            else:

                result = {
                    "status": "info",
                    "message": f"{step['agent']} not implemented."
                }

            results.append(result)

            # Save the latest response returned by an agent
            if isinstance(result, dict):
                if "result" in result:
                    final_response = result["result"]
                elif "message" in result:
                    final_response = result["message"]

        return {
            "response": final_response,
            "plan": plan["steps"],
            "results": results
        }