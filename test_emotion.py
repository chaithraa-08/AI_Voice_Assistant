from emotion import EmotionDetector

detector = EmotionDetector()

while True:
    text = input("You: ")

    if text.lower() == "exit":
        break

    result = detector.detect(text)

    print(f"Emotion   : {result['emotion']}")
    print(f"Confidence: {result['confidence']}")
    print("-" * 40)