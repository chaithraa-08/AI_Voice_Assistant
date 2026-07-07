from groq import Groq
from dotenv import load_dotenv
import os

from tool_registry import tools
from tool_executer import execute_tool

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI voice assistant."
    }
]

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add user message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # First call to Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # ----------------------------
    # Did Groq request a tool?
    # ----------------------------
    if message.tool_calls:

        tool_call = message.tool_calls[0]

        print("\nTool Requested:", tool_call.function.name)

        # Execute the requested tool
        tool_result = execute_tool(tool_call)

        print("Tool Result:", tool_result)

        # Add assistant message containing tool call
        messages.append(message)

        # Add tool response
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
            }
        )

        # Ask Groq again using tool result
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        assistant_reply = final_response.choices[0].message.content

    else:
        assistant_reply = message.content

    print("\nAssistant:", assistant_reply)

    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )