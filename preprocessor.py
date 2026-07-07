import re

def preprocess(text):
    text = text.lower()

    # Math normalization
    replacements = {
        "multiplied by": "*",
        "multiply by": "*",
        "times": "*",
        " x ": " * ",
        "into ": "*",
        "plus": "+",
        "minus": "-",
        "divided by": "/",
        "divide by": "/",
        "over": "/",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()