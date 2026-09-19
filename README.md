# Streamlit Learning

A small task tracker built while learning [Streamlit](https://streamlit.io). Tasks are entered through a form and stored in a local SQLite database. The app is structured as a multipage Streamlit app (`st.navigation`), so pages live under `pages/` instead of all being in `main.py`.

## Features

- Add tasks with a name, description, due date, status and priority (0-5)
- Status defaults to `Pending` and is restricted to `Pending`, `Active`, `On Hold`, or `Completed`
- Tasks are saved to a SQLite database (`data/tasks.db`, created automatically on first run)
- All saved tasks are shown in a table below the form

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | Entry point: initializes the database and sets up `st.navigation` across the app's pages |
| `pages/task_page.py` | The task page: add-task form and task table |
| `tools/database.py` | SQLite helpers: creates/updates the table, adds tasks, updates tasks, reads tasks |
| `data/` | Holds the SQLite database (`tasks.db`, git-ignored) |
| `docs/notes.md` | Personal setup and learning notes |

Note: with only one page registered in `st.navigation`, Streamlit hides the sidebar navigation widget by default — it reappears automatically once a second page is added.

## Setup

Requires Python 3.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install streamlit pandas
```

## Run

Streamlit apps are started with `streamlit run`, not by running the file directly:

```powershell
streamlit run main.py
```

Then open the URL it prints (usually http://localhost:8501).

## How the database works

`tools/database.py`'s `init_db()` runs on every start. It creates the `tasks` table if it doesn't exist and adds any columns listed in `COLUMNS` that are missing.

Adding a `CHECK` constraint to an existing column isn't possible with this approach. If you change a constraint, drop the table (or delete `data/tasks.db`) and let the app recreate it.

Available helpers:

- `add_task(task_name, task_description, due_date, priority, status="Pending")` — inserts a new task
- `update_task(id, column_name, value)` — updates a single column on one row by id (`column_name` is validated against `COLUMNS`)
- `set_task_completed(id)` — marks a task completed, stamping `completed_timestamp` and setting `status` to `Completed`
- `get_tasks()` — returns all tasks as a DataFrame
