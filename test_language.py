from language import detect_language

texts = [
    "Hello, how are you today?",
    "नमस्ते आप कैसे हैं",
    "ನಮಸ್ಕಾರ ನೀವು ಹೇಗಿದ್ದೀರಿ",
    "హలో మీరు ఎలా ఉన్నారు"
]

for text in texts:
    code, language = detect_language(text)

    print(f"Text      : {text}")
    print(f"Code      : {code}")
    print(f"Language  : {language}")
    print("-" * 40)