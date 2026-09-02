import re


def clean_text(text: str) -> str:
    """Normalize whitespace and remove control characters from extracted resume text."""
    text = re.sub(r"\x00|\ufeff", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"
