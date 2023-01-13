import sqlite3
import os

conn = sqlite3.connect(os.path.join("database", "birthday.db"))
cursor = conn.cursor()


def is_user_exist_in_base(user_id: int) -> bool:
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {user_id}")
    user_exists = cursor.fetchall()
    if user_exists:
        return True
    return False


def new_user(user_id: int) -> None:
    cursor.execute(f"INSERT INTO users(tg_id, active) VALUES ({user_id}, 1)")
    conn.commit()


def _init_db():
    """Инициализирует БД"""
    with open(os.path.join("database", "createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='users'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
