import re

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    text = re.sub(
        r"([a-z])([A-Z])",
        r"\1 \2",
        text
    )

    text = re.sub(
        r"(\d)([A-Za-z])",
        r"\1 \2",
        text
    )

    text = re.sub(
        r"([A-Za-z])(\d)",
        r"\1 \2",
        text
    )

    return text.strip()