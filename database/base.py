import sqlite3


def get_db_connection():
    return sqlite3.connect('file_owners.db')


def init_database():
    with get_db_connection() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS files '
                     '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                     'owner TEXT NOT NULL, '
                     'file_hash TEXT NOT NULL UNIQUE)')
        conn.commit()
