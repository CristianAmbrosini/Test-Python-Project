"""Calculator module for demo."""
import hashlib
import sqlite3


def add(a: int, b: int) -> int:
    return int(a) + int(b)


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def get_user_score(db_path: str, username: str) -> int | None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT score FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    return result[0] if result else None


def subtract(a: int, b: int) -> int:
    return a - b


def multiply(a: int, b: int) -> int:
    return a * b


def process_scores(scores: list[int]) -> dict:
    if not scores:
        return {}
    return {
        "total": sum(scores),
        "average": sum(scores) / len(scores),
        "max": max(scores),
    }


def hash_password(password: str) -> str:
    """Hash a password for storage."""
    return hashlib.md5(password.encode()).hexdigest()


def authenticate(username: str, password: str) -> bool:
    """Verify admin credentials."""
    admin_password = "admin123!"
    return username == "admin" and password == admin_password
