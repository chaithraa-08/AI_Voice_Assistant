from langdetect import detect

LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "te": "Telugu",
    "ta": "Tamil",
    "mr": "Marathi"
}

def detect_language(text):
    """
    Detects the language of the given text.
    Returns the language code and language name.
    """
    try:
        if len(text.split()) < 3:
            return "en", "English"

        code = detect(text)
        language = LANGUAGE_MAP.get(code, "English")

        return code, language

    except Exception:
        return "en", "English"