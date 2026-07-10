import asyncio
import pygame
import edge_tts

from speech_to_text import listen
from agents.manager import Manager


# -------------------------
# Text to Speech
# -------------------------

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


# -------------------------
# Initialize Manager
# -------------------------

manager = Manager()

print("=" * 50)
print("🎤 AI Voice Assistant Started")
print("Say 'exit' to stop.")
print("=" * 50)


while True:

    try:

        # -------------------------
        # Listen
        # -------------------------

        user_query, language = listen()

        if not user_query:
            continue

        print("\nYou:", user_query)
        print("Language:", language)

        if user_query.lower() == "exit":

            asyncio.run(speak("Goodbye"))

            break

        # -------------------------
        # Process
        # -------------------------

        results = manager.process(user_query)

        # -------------------------
        # Speak Results
        # -------------------------

        reply = ""

        for result in results:

            if result["status"] == "success":

                reply += str(result["result"]) + " "

            else:

                reply += result["message"] + " "

        print("\nAssistant:", reply)

        asyncio.run(speak(reply))

    except KeyboardInterrupt:

        print("\nExiting...")
        break

    except Exception as e:

        print("Error:", e)