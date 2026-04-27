"""String utility functions."""


def reverse_words(sentence: str) -> str:
    return " ".join(sentence.split()[::-1])


def count_vowels(text: str) -> int:
    return sum(1 for c in text.lower() if c in "aeiou")


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def to_snake_case(text: str) -> str:
    result = []
    for i, char in enumerate(text):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def is_palindrome(text: str) -> bool:
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]
