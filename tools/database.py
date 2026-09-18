import sqlite3
from pathlib import Path

import pandas as pd

# <project root>/data/tasks.db, independent of where Streamlit is launched from
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Columns the tasks table should have (name -> definition).
# To add a column later, just add a line here. NOT NULL columns need a DEFAULT.
COLUMNS = {
    "task_name": "TEXT NOT NULL DEFAULT ''",
    "task_description": "TEXT",
    "due_date": "TEXT NOT NULL DEFAULT ''",
    "status": "INTEGER NOT NULL DEFAULT 0",
    "priority": "INTEGER DEFAULT 0 CHECK (priority BETWEEN 0 AND 5)",
}

# Initializing database: create the table if missing, then add any missing columns.
def init_db():
    conn = get_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT)")

    existing = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
    for name, definition in COLUMNS.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE tasks ADD COLUMN {name} {definition}")

    conn.commit()
    conn.close()


# Adding task to database
def add_task(task_name, task_description, due_date, status, priority):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (task_name, task_description, due_date, status, priority) VALUES (?, ?, ?, ?, ?)",
        (task_name, task_description, due_date, status, priority),
    )
    conn.commit() # Commiting
    conn.close()

def get_tasks():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return df
