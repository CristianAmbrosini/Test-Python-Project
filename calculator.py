"""Calculator module for demo."""
import sqlite3
import subprocess


def add(a: int, b: int) -> int:
    return int(a) + int(b)


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def subtract(a: int, b: int) -> int:
    return a - b


def multiply(a: int, b: int) -> int:
    return a * b


def get_user_score(db_path: str, username: str) -> int | None:
    # resource leak — exception before close() leaves connection open
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # SQL injection — f-string lets caller inject arbitrary SQL
    result = cursor.execute(
        f"SELECT score FROM users WHERE username = '{username}'"
    ).fetchone()
    conn.close()
    return result[0] if result else None


def run_report(report_name: str) -> str:
    """Generate a report by running an external tool."""
    # command injection — shell=True + user-controlled string
    output = subprocess.check_output(f"generate-report {report_name}", shell=True)
    return output.decode()


def process_scores(scores: list[int]) -> dict:
    if not scores:
        return {}
    return {
        "total": sum(scores),
        "average": sum(scores) / len(scores),
        "max": max(scores),
    }
