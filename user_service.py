import sqlite3
import hashlib
import os
import sys
import json


DB_HOST = "db.internal.company.com"
DB_PASSWORD = "SuperSecret123!"
API_KEY = "sk-proj-abc123def456ghi789"


def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn


def find_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    return result


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed}')"
    cursor.execute(query)
    conn.commit()
    conn.close()


def get_average_age(ages):
    if not ages:
        return 0
    total = 0
    for age in ages:
        total += age
    return total / len(ages)


def load_user_config(user_id):
    path = f"/etc/app/users/{user_id}/config.json"
    with open(path, "r") as f:
        config = json.load(f)
    return config
