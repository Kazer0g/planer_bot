import logging
import sqlite3

db_path = 'bot/db.db'
logging.basicConfig(level=logging.INFO)
def connect_db():
    global conn, cursor
    logging.info('Connecting to SQLite...')
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    logging.info('Connected to SQLite')
    return conn, cursor

def add_user(id, username):
    user_name = cursor.execute(
        "SELECT username FROM users WHERE id = ?",
        (id,)
    ).fetchall()
    if len(user_name) == 0:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?)", 
            (id, username)
            )
        conn.commit()
        logging.info(f'{username}:{id} added')
    else:
        logging.info(f'{username}:{id} already exists')

def add_task(owner_id, name, description='Нет описания', deadline='Нет дедлайна'):
    cursor.execute(
        "INSERT INTO tasks VALUES (?, ?, ?)",
        (owner_id, description, deadline)
    )
    conn.commit()
    logging.info(f"{name} task added, owner:{owner_id}, description:{description}, deadline:{deadline}")

def get_task(id):
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )
    return cursor.fetchall()

def get_tasks(id):
    cursor.execute(
        "SELECT * FROM tasks WHERE owner_id = ?",
        (id,)
    )
    return cursor.fetchall()