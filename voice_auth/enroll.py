import os
import sounddevice as sd
import soundfile as sf
import torch
from scipy.io.wavfile import write
from speechbrain.inference.speaker import EncoderClassifier



# -----------------------------
# Load SpeechBrain Model
# -----------------------------
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)

# -----------------------------
# User Name
# -----------------------------
name = input("Enter your name: ").strip()

os.makedirs("voice_profiles", exist_ok=True)

filename = f"voice_profiles/{name}.wav"

# -----------------------------
# Record Voice
# -----------------------------
duration = 10      # seconds
sample_rate = 16000

print("\nSpeak normally for 10 seconds...")
print("Recording...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()

write(filename, sample_rate, audio)

print(f"\nVoice sample saved as {filename}")

# -----------------------------
# Generate Voice Embedding
# -----------------------------
# Load the recorded audio
signal, sample_rate = sf.read(filename)

signal = torch.tensor(signal, dtype=torch.float32)

# Convert to [1, time]
if signal.dim() == 1:
    signal = signal.unsqueeze(0)
else:
    signal = signal.mean(dim=1).unsqueeze(0)

# Generate embedding
with torch.no_grad():
    embedding = classifier.encode_batch(signal)

# Save embedding
embedding_file = f"voice_profiles/{name}.pt"
torch.save(embedding.squeeze(), embedding_file)

print("\n✅ Voice profile created successfully!")