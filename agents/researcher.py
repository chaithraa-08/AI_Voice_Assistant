from tools.search import web_search
from tools.weather import get_weather


class ResearchAgent:

    def execute(self, step):

        tool = step["tool"]
        parameters = step["parameters"]

        try:

            if tool == "search":

                query = parameters.get("query")
                result = web_search(query)

            elif tool == "weather":

                city = parameters.get("location")
                result = get_weather(city)

            else:

                return {
                    "status": "error",
                    "message": f"Unknown research tool: {tool}"
                }

            return {
                "status": "success",
                "result": result
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }