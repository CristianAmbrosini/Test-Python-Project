import hashlib
import sqlite3
import subprocess


# Hardcoded credentials — noncompliant
DB_PASSWORD = "supersecret123"
API_KEY = "sk-prod-abc123xyz"


def hash_password(password):
    # Noncompliant: MD5 is cryptographically weak
    return hashlib.md5(password.encode()).hexdigest()


def get_user(conn, user_id):
    # Noncompliant: SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    cursor = conn.execute(query)
    return cursor.fetchone()


def run_report(report_name):
    # Noncompliant: command injection
    result = subprocess.run("generate_report.sh " + report_name, shell=True, capture_output=True)
    return result.stdout


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def process_payment(amount, currency):
    if currency == "USD":
        rate = 1.0
    elif currency == "EUR":
        rate = 1.1
    else:
        raise ValueError(f"Unsupported currency: {currency}")
    converted = amount * rate
    return converted


def connect():
    # Noncompliant: hardcoded credentials passed directly
    conn = sqlite3.connect(f"file:db?password={DB_PASSWORD}", uri=True)
    return conn
