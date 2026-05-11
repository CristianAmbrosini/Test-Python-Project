def reverse(s: str) -> str:
    return s[::-1]


def capitalize_words(s: str) -> str:
    return " ".join(word.capitalize() for word in s.split())


def truncate(s: str, max_length: int, suffix: str = "...") -> str:
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix
