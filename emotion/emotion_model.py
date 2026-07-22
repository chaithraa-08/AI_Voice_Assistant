import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class EmotionModel:

    def __init__(self):

        self.tokenizer = AutoTokenizer.from_pretrained(
            "j-hartmann/emotion-english-distilroberta-base"
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            "j-hartmann/emotion-english-distilroberta-base"
        )

        self.labels = self.model.config.id2label

    def predict(self, text: str):

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.softmax(outputs.logits, dim=1)[0]

        results = []

        for i, score in enumerate(probabilities):
            results.append({
                "emotion": self.labels[i],
                "confidence": round(score.item(), 3)
            })

        results.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return {
            "emotion": results[0]["emotion"],
            "confidence": results[0]["confidence"],
            "top3": results[:3]
        }