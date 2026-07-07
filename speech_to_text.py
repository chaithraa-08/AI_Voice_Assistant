import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import tempfile
import os

# Load Whisper model only once
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def listen():
    """
    Records audio from the microphone and returns:
    text, detected_language
    """

    duration = 5          # seconds
    sample_rate = 16000

    print("🎤 Listening...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype=np.int16
    )

    sd.wait()

    # Save temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:

        write(temp_audio.name, sample_rate, recording)

        temp_filename = temp_audio.name

    # Transcribe
    segments, info = model.transcribe(temp_filename)

    text = ""

    for segment in segments:
        text += segment.text

    os.remove(temp_filename)

    return text.strip(), info.language