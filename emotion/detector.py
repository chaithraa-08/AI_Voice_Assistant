from emotion.emotion_model import EmotionModel


class EmotionDetector:

    def __init__(self):
        self.model = EmotionModel()

    def detect(self, text):
        return self.model.predict(text)