import json

from tools.weather import get_weather
from tools.calculator import calculate
from tools.search import web_search


def execute_tool(tool_call):
    """
    Executes the tool requested by Groq.
    """

    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print(f"\nTool Called: {function_name}")
    print(f"Arguments : {arguments}")

    if function_name == "get_weather":
        return get_weather(arguments["city"])

    elif function_name == "calculate":
        return calculate(arguments["expression"])

    elif function_name == "web_search":
        return web_search(arguments["query"])

    return "Unknown Tool"