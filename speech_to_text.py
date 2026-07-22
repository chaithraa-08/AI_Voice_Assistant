import os
import tempfile

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

from emotion import EmotionDetector


# -----------------------------------------
# Load Whisper Model (Only Once)
# -----------------------------------------
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# -----------------------------------------
# Load Emotion Detector (Only Once)
# -----------------------------------------
emotion_detector = EmotionDetector()


def listen():
    """
    Records audio from the microphone and returns:

        text
        detected_language
        detected_emotion
    """

    duration = 5
    sample_rate = 16000

    print("\n🎤 Listening...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype=np.int16
    )

    sd.wait()

    # Save temporary audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:

        write(temp_audio.name, sample_rate, recording)

        temp_filename = temp_audio.name

    # Whisper transcription
    segments, info = model.transcribe(temp_filename)

    text = ""

    for segment in segments:
        text += segment.text

    # Delete temporary file
    os.remove(temp_filename)

    text = text.strip()

    # Detect Emotion
    emotion = emotion_detector.detect(text)

    return text, info.language, emotion