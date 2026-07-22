import os
import torch
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

classifier = None

# Load SpeechBrain model only once


def verify_user(name="Chaithra", threshold=0.65):
    """
    Verify the speaker's voice.

    Returns:
        True  -> Voice verified
        False -> Voice verification failed
    """

    global classifier

    if classifier is None:
        from speechbrain.inference.speaker import EncoderClassifier

        classifier = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )

    embedding_file = f"voice_profiles/{name}.pt"

    if not os.path.exists(embedding_file):
        print("❌ Voice profile not found.")
        return False

    saved_embedding = torch.load(embedding_file)

    duration = 5
    sample_rate = 16000

    print("\n🎤 Voice Authentication")
    print("Speak for verification...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    temp_file = "voice_profiles/temp.wav"
    write(temp_file, sample_rate, audio)

    signal, sr = sf.read(temp_file)

    signal = torch.tensor(signal, dtype=torch.float32)

    if signal.dim() == 1:
        signal = signal.unsqueeze(0)
    else:
        signal = signal.mean(dim=1).unsqueeze(0)

    with torch.no_grad():
        new_embedding = classifier.encode_batch(signal)

    new_embedding = new_embedding.squeeze()

    similarity = torch.nn.functional.cosine_similarity(
        saved_embedding.unsqueeze(0),
        new_embedding.unsqueeze(0)
    )

    score = similarity.item()

    print(f"Similarity Score: {score:.4f}")

    if score >= threshold:
        print("✅ Voice Verified")
        return True
    else:
        print("❌ Voice Verification Failed")
        return False