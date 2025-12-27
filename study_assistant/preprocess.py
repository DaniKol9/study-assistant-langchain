"""
Text preprocessing utilities.

Handles cleanup of PDF extraction artifacts such as excessive newlines,
hyphenated line breaks, and inconsistent spacing.
"""


import re

def repair_newlines(text: str) -> str:
    # Normalize line endings
    text = text.replace("\r", "\n")

    # If a line break is NOT followed by another line break, treat it like a space.
    # This keeps paragraph breaks (double newlines) intact.
    text = re.sub(r"\n(?!\n)", " ", text)

    # Now collapse any leftover multiple blank lines to max two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Clean up extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)            # collapse spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text)         # collapse huge blank gaps
    text = re.sub(r"-\n(\w+)", r"\1", text)        # fix simple hyphen line breaks
    return text.strip()