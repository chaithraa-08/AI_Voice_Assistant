import os
import torch
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
from speechbrain.inference.speaker import EncoderClassifier

# -----------------------------
# Load SpeechBrain model
# -----------------------------
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)

# -----------------------------
# User name
# -----------------------------
name = input("Enter your name: ").strip()

embedding_file = f"voice_profiles/{name}.pt"

if not os.path.exists(embedding_file):
    print("❌ Voice profile not found.")
    exit()

saved_embedding = torch.load(embedding_file)

# -----------------------------
# Record new voice
# -----------------------------
duration = 5
sample_rate = 16000

print("\nSpeak for verification...")
print("Recording...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()

temp_file = "voice_profiles/temp.wav"
write(temp_file, sample_rate, audio)

# -----------------------------
# Load recorded audio
# -----------------------------
signal, sr = sf.read(temp_file)

signal = torch.tensor(signal, dtype=torch.float32)

if signal.dim() == 1:
    signal = signal.unsqueeze(0)
else:
    signal = signal.mean(dim=1).unsqueeze(0)

# -----------------------------
# Generate embedding
# -----------------------------
with torch.no_grad():
    new_embedding = classifier.encode_batch(signal)

new_embedding = new_embedding.squeeze()

# -----------------------------
# Compare embeddings
# -----------------------------
similarity = torch.nn.functional.cosine_similarity(
    saved_embedding.unsqueeze(0),
    new_embedding.unsqueeze(0)
)

score = similarity.item()

print(f"\nSimilarity Score: {score:.4f}")

THRESHOLD = 0.65

if score > THRESHOLD:
    print("✅ Voice Verified")
else:
    print("❌ Voice Verification Failed")