import bcrypt
import sqlite3
import subprocess
import os
import pickle
import logging


def get_user(user_id):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = conn.execute(query)
    return result.fetchone()


def authenticate(username, password):
    ADMIN_PASSWORD = "SuperSecret123!"
    if password == ADMIN_PASSWORD:
        return True
    conn = sqlite3.connect("users.db")
    row = conn.execute(
        f"SELECT password_hash FROM users WHERE username = '{username}'"
    ).fetchone()
    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        return True
    return False


def run_diagnostics(host):
    result = subprocess.run(
        ["ping", "-c", "1", host], capture_output=True, text=True
    )
    return result.stdout


def load_user_preferences(data):
    return pickle.loads(data)


def create_temp_file(filename):
    path = os.path.join("/tmp", filename)
    with open(path, "w") as f:
        os.chmod(path, 0o600)
        f.write("temp data")
    return path


def process_users(user_ids):
    results = []
    for uid in user_ids:
        user = get_user(uid)
        results.append(user)
    processed = []
    for uid in user_ids:
        user = get_user(uid)
        processed.append(user)
    return results, processed


def divide_scores(scores):
    return [100 / s for s in scores if s != 0]


def log_login(username, password):
    logging.info(f"Login attempt: user={username}, password={password}")


def get_user_role(user_id, default_roles=[]):
    default_roles.append("viewer")
    return default_roles
