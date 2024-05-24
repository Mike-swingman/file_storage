from database.base import get_db_connection


def insert_file_record(owner, hash_filename):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO files (owner, file_hash) VALUES (?, ?)', (owner, hash_filename))
        conn.commit()


def is_owner_file(hash_filename, user):
    with get_db_connection() as conn:
        result = conn.execute('SELECT owner FROM files WHERE file_hash = ?', (hash_filename,)).fetchone()
    return result is not None and result[0] == user


def delete_file_record(hash_filename):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM files WHERE file_hash = ?', (hash_filename,))
        conn.commit()
