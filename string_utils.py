"""String utility helpers."""


def truncate(s: str, max_length: int) -> str:
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    return s[:max_length]


def capitalize_words(s: str) -> str:
    return ' '.join(word.capitalize() for word in s.split())


def count_vowels(s: str) -> int:
    return sum(1 for c in s.lower() if c in 'aeiou')


def reverse_words(s: str) -> str:
    return ' '.join(s.split()[::-1])


def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
