import os
import sqlite3
import hashlib

# Docker Compose에서는 DB_PATH 환경변수로 볼륨 경로를 지정 (예: /app/data/app.db)
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "app.db"))


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS taken_courses (
            username TEXT NOT NULL,
            course_code TEXT NOT NULL,
            PRIMARY KEY (username, course_code)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_courses (
            username TEXT NOT NULL,
            course_code TEXT NOT NULL,
            PRIMARY KEY (username, course_code)
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """간단한 단방향 해시. 실습 목적이므로 salt 없이 sha256만 사용합니다."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------
# 사용자
# ---------------------------------------------------------------
def get_user(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def create_user(username: str, password: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hash_password(password)),
    )
    conn.commit()
    conn.close()


def verify_user(username: str, password: str) -> bool:
    user = get_user(username)
    if user is None:
        return False
    return user["password_hash"] == hash_password(password)


# ---------------------------------------------------------------
# 이미 들은 과목 (taken courses)
# ---------------------------------------------------------------
def get_taken_codes(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT course_code FROM taken_courses WHERE username = ?", (username,))
    codes = {row["course_code"] for row in cur.fetchall()}
    conn.close()
    return codes


def add_taken_code(username: str, course_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO taken_courses (username, course_code) VALUES (?, ?)",
        (username, course_code),
    )
    conn.commit()
    conn.close()


def remove_taken_code(username: str, course_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM taken_courses WHERE username = ? AND course_code = ?",
        (username, course_code),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------
# 저장한 강의 (saved / 찜 목록)
# ---------------------------------------------------------------
def get_saved_codes(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT course_code FROM saved_courses WHERE username = ?", (username,))
    codes = [row["course_code"] for row in cur.fetchall()]
    conn.close()
    return codes


def add_saved_code(username: str, course_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO saved_courses (username, course_code) VALUES (?, ?)",
        (username, course_code),
    )
    conn.commit()
    conn.close()


def remove_saved_code(username: str, course_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM saved_courses WHERE username = ? AND course_code = ?",
        (username, course_code),
    )
    conn.commit()
    conn.close()
