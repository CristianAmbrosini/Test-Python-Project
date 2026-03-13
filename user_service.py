import hashlib
import sqlite3
import os

DB_USERNAME = "admin"
DB_PASSWORD = "SuperSecret123!"
DB_HOST = "prod-db.internal.company.com"
API_KEY = "sk-live-4f3c2b1a0d9e8f7g6h5i4j3k2l1m0n"

def get_db_connection():
    conn = sqlite3.connect(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/users_db")
    return conn

def login(username, password):
    hashed = hashlib.md5(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{hashed}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Login successful for {username} with password {password}")
        return {"status": "ok", "user_id": user[0], "token": API_KEY}
    else:
        print(f"Login failed for {username}, tried password: {password}")
        return {"status": "error"}

def get_user_data(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM user_data WHERE user_id = '" + str(user_id) + "'"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        conn.commit()
        conn.close()
    except:
        pass

def export_user_report(user_id):
    data = get_user_data(user_id)
    report_path = f"/tmp/report_{user_id}.txt"
    with open(report_path, "w") as f:
        f.write(str(data))
    os.chmod(report_path, 0o777)
    return report_path

def update_password(user_id, new_password):
    new_hash = hashlib.sha1(new_password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET password_hash = '{new_hash}' WHERE id = {user_id}")
    conn.commit()
    conn.close()
    print(f"Password updated for user {user_id}, new hash: {new_hash}")

def search_users(name_filter):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE '%" + name_filter + "%'")
    results = cursor.fetchall()
    conn.close()
    return results
