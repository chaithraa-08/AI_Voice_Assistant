from speech_to_text import listen

text, language = listen()

print("\nDetected Language:", language)
print("Recognized Text:", text)