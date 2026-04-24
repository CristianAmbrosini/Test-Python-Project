def normalize_whitespace(text):
    return ' '.join(text.split())


def to_snake_case(text):
    result = []
    for i, char in enumerate(text):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    return ''.join(result)


def count_words(text):
    if not text.strip():
        return 0
    return len(text.split())


def pad_left(text, width, char=' '):
    if len(text) >= width:
        return text
    return char * (width - len(text)) + text


def reverse_words(text):
    return ' '.join(text.split()[::-1])
