from groq import Groq
from dotenv import load_dotenv
import os
import speech_recognition as sr
import edge_tts
import asyncio
import pygame
from preprocessor import preprocess
from camera_tools import take_photo
from language import detect_language
from tool_registry import tools
from tool_executer import execute_tool
from app_launcher import (
    open_app
)

# Load API Key
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Speech Recognition
recognizer = sr.Recognizer()

# Conversation Memory
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI voice assistant. "
            "Keep responses short, natural, and conversational."
        )
    }
]


# Text-to-Speech Function
async def speak(text):
    filename = "response.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-JennyNeural"
    )

    await communicate.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()


print("🎤 AI Voice Assistant Started")
print("Say 'exit' to stop.\n")

while True:

    try:

        with sr.Microphone() as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(source)

        user_text = recognizer.recognize_google(audio)

        print("Original:", user_text)

        user_text = preprocess(user_text)

        print("Processed:", user_text)

        # Detect language
        language_code, language_name = detect_language(user_text)

        print(f"Detected Language: {language_name}")
        
        if user_text.lower().startswith("open"):

            app_name = user_text.lower().replace("open", "", 1).strip()

            if not app_name:
                response = "Please tell me what you want me to open."

                print("Assistant:", response)

                asyncio.run(speak(response))

                continue

            result = open_app(app_name)

            print("Assistant:", result)

            asyncio.run(speak(result))

            continue

        if "take photo" in user_text.lower():

            result = take_photo()

            print("Assistant:", result)

            asyncio.run(speak(result))

            continue

        if user_text.lower() == "exit":

            print("Goodbye!")

            asyncio.run(speak("Goodbye!"))

            break

        # Store User Message
        messages.append(
            {
                "role": "user",
                "content": user_text
            }
        )
        messages[0]["content"] = (
            "You are a helpful AI voice assistant. "
            "Keep responses short, natural, and conversational. "
            f"Always reply in {language_name}."
        )
        # Send to Groq
        # First call to Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Check if Groq wants to use a tool
        if message.tool_calls:

            tool_call = message.tool_calls[0]

            print(f"\nTool Requested: {tool_call.function.name}")

            # Execute the tool
            tool_result = execute_tool(tool_call)

            print("Tool Result:", tool_result)

            # Store assistant tool call
            messages.append(message)

            # Store tool result
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                }
            )

            # Ask Groq again using the tool result
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )

            assistant_reply = final_response.choices[0].message.content

        else:

            assistant_reply = message.content

        print("Assistant:", assistant_reply)

        # Speak the response
        asyncio.run(speak(assistant_reply))

        # Save conversation
        messages.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

    except sr.UnknownValueError:

        print("Sorry, I couldn't understand that.")

    except sr.RequestError:

        print("Speech Recognition service unavailable.")

    except Exception as e:

        print("Error:", e)