import sqlite3


def create_connection():
    connection = sqlite3.connect("database.db")
    return connection


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        Create table if not exists employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        gender TEXT NOT NULL,
        job_title TEXT NOT NULL,
        salary FLOAT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
