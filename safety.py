# safety.py

banned_words = [
    "kill", "harm humans", "weapon", "illegal",
    "hate", "offensive", "bomb", "suicide", "nigger", "fuck", "bitch",
]

def is_safe(text: str) -> bool:
    text_lower = text.lower()
    for word in banned_words:
        if word in text_lower:
            return False
    return True
