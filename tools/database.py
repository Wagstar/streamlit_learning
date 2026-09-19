import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime



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
    "status": "TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Active', 'On Hold', 'Completed'))",
    "priority": "INTEGER DEFAULT 0 CHECK (priority BETWEEN 0 AND 5)",
    "created_timestamp": "TEXT NOT NULL DEFAULT ''",
    "completed_timestamp": "TEXT",
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
def add_task(task_name, task_description, due_date, priority, status="Pending"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (task_name, task_description, due_date, status, priority,created_timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (task_name, task_description, due_date, status, priority, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit() # Commiting
    conn.close()

def update_task(id, column_name, value):
    if column_name not in COLUMNS:
        raise ValueError(f"Invalid column name: {column_name}")
    conn = get_connection()
    conn.execute(
        f"UPDATE tasks SET {column_name} = ? WHERE id = ?",
        (value, id),
    )
    conn.commit() # Commiting query
    conn.close()

def set_task_completed(id):
    conn = get_connection()
    conn.execute(
        "UPDATE tasks SET (completed_timestamp, status) VALUES (?,?) WHERE id = ?",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Completed", id),
    )
    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return df

