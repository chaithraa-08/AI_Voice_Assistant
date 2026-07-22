import asyncio
import pygame
import edge_tts

from voice_auth.auth import verify_user
from speech_to_text import listen
from agents.manager import Manager


# -----------------------------------------
# Text-to-Speech
# -----------------------------------------
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


# -----------------------------------------
# Voice Authentication
# -----------------------------------------
print("=" * 50)
print("🔐 Voice Authentication")
print("=" * 50)

if not verify_user():
    print("Access Denied!")
    exit()

print("Access Granted!")


# -----------------------------------------
# Initialize Manager
# -----------------------------------------
manager = Manager()

print("=" * 50)
print("🎤 AI Voice Assistant Started")
print("Say 'exit' to stop.")
print("=" * 50)


# -----------------------------------------
# Main Loop
# -----------------------------------------
while True:

    try:

        user_query, language, emotion = listen()

        if not user_query:
            print("⚠️ No speech detected.")
            continue

        print("\nYou:", user_query)
        print("Language:", language)
        print("Emotion:", emotion["emotion"])
        print("Confidence:", emotion["confidence"])

        if user_query.lower() == "exit":

            asyncio.run(speak("Goodbye"))

            break

        # Process User Query
        response = manager.process(
            user_query,
            emotion
        )

        reply = response["response"]

        print("\nAssistant:", reply)

        asyncio.run(speak(reply))

    except KeyboardInterrupt:

        print("\nExiting...")
        break

    except Exception as e:

        print("\n❌ Error:", e)