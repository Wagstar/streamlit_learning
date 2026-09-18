# Streamlit Learning

A small task tracker built while learning [Streamlit](https://streamlit.io). Tasks are entered through a form and stored in a local SQLite database.

## Features

- Add tasks with a name, description, due date, status and priority (0-5)
- Tasks are saved to a SQLite database (`data/tasks.db`, created automatically on first run)
- All saved tasks are shown in a table below the form

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | The Streamlit app: form and task table |
| `tools/database.py` | SQLite helpers: creates/updates the table, adds tasks, reads tasks |
| `data/` | Holds the SQLite database (`tasks.db`, git-ignored) |
| `docs/notes.md` | Personal setup and learning notes |

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
