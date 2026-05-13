from typing import Optional


def find_max(numbers: list[int]) -> Optional[int]:
    if not numbers:
        return None
    return max(numbers)


def flatten(nested: list[list]) -> list:
    return [item for sublist in nested for item in sublist]

