from speechbrain.inference.speaker import SpeakerRecognition

print("Loading SpeechBrain model...")

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)

print("✅ Model Loaded Successfully!")