import logging
import sqlite3

db_path = 'bot/db.db'
logging.basicConfig(level=logging.INFO)

# * DB
def connect_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    global conn, cursor
    logging.info('Connecting to SQLite...')
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    logging.info('Connected to SQLite')
    return conn, cursor

def get_message_id(id) -> int:
    cursor.execute(
        "SELECT message_id FROM users WHERE id = ?",
        (id,)
    )
    return cursor.fetchall()[0][0]

# * Users
def add_user(id, username, message_id):
    data = cursor.execute(
        "SELECT username FROM users WHERE id = ?",
        (id,)
    ).fetchall()
    if len(data) == 0:
        if username == None:
            username = 'Secret'
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)", 
            (id, username, message_id)
            )
        logging.info(f'{username}:{id} added')
    else:
        cursor.execute(
            "UPDATE users SET message_id = ? WHERE id = ?",
            (message_id, id)
        )
        logging.info(f'{username}:{id} already exists')
    conn.commit()
# * Lists
def add_list(owner_id, name):
    cursor.execute(
        "INSERT INTO lists (owner_id, name) VALUES (?, ?)",
        (owner_id, name)
    )
    conn.commit()
    logging.info(f"{name} list added, owner:{owner_id}")
def delete_list(id):
    cursor.execute(
        "DELETE FROM lists WHERE id = ?",
        (id,)
    )
    conn.commit()
    logging.info(f"List {id} deleted")
    # TODO: delete all tasks
def get_lists_ids(owner_id):
    cursor.execute(
        "SELECT id FROM lists WHERE owner_id = ?",
        (owner_id,)
    )
    return cursor.fetchall()
def get_list_name(list_id) -> str:
    cursor.execute(
        "SELECT name FROM lists WHERE id = ?",
        (list_id,)
    )
    return str(cursor.fetchall()[0][0])


# * Tasks
def add_task(owner_id, list_id, name, description='Нет описания', deadline='Нет дедлайна'):
    cursor.execute(
        "INSERT INTO tasks (owner_id, list_id, name, description, deadline) VALUES (?, ?, ?, ?, ?)",
        (owner_id, list_id, name, description, deadline)
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
        "SELECT * FROM tasks WHERE list_id = ?",
        (id,)
    )
    return cursor.fetchall()