from tools.calculator import calculate
from tools.weather import get_weather
from tools.search import web_search
from tools.app_launcher import launch_app
from tools.browser import browser_execute
from tools.camera import camera_execute
from tools.file_manager import file_manager_execute
from tools.system_control import system_control_execute


class ExecutorAgent:

    def __init__(self):

        self.tools = {
            "calculator": calculate,
            "weather": get_weather,
            "search": web_search,
            "app_launcher": launch_app,
            "browser": browser_execute,
            "camera": camera_execute,
            "file_manager": file_manager_execute,
            "system_control": system_control_execute
        }

    def execute(self, step):

        tool = step["tool"]
        action = step.get("action", "")
        parameters = step.get("parameters", {})

        if tool not in self.tools:
            return {
                "status": "error",
                "message": f"Tool '{tool}' not available."
            }

        try:

            # Calculator
            if tool == "calculator":
                expression = parameters.get("expression")
                result = calculate(expression)

            # Weather
            elif tool == "weather":
                location = parameters.get("location")
                result = get_weather(location)

            # Internet Search
            elif tool == "search":
                query = parameters.get("query")
                result = web_search(query)

            # App Launcher
            elif tool == "app_launcher":
                app = parameters.get("app")
                result = launch_app(app)

            # Browser
            elif tool == "browser":
                result = browser_execute(action, parameters)

            # Camera
            elif tool == "camera":
                result = camera_execute(action, parameters)

            # File Manager
            elif tool == "file_manager":
                result = file_manager_execute(action, parameters)

            # System Control
            elif tool == "system_control":
                result = system_control_execute(action, parameters)

            else:
                return {
                    "status": "error",
                    "message": f"Unknown tool '{tool}'."
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