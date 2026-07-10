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

        plan = self.planner.create_plan(user_query)

        results = []

        for step in plan["steps"]:

            if step["agent"] == "ExecutorAgent":

                result = self.executor.execute(step)

            elif step["agent"] == "ResearchAgent":

                result = self.researcher.execute(step)

            elif step["agent"] == "ChatAgent":

                result = self.chat.execute(step)

            else:

                result = {
                    "status": "info",
                    "message": f"{step['agent']} not implemented."
                }

            results.append(result)

        return results