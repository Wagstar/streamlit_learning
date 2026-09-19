# Streamlit Learning

A small task tracker built while learning [Streamlit](https://streamlit.io). Tasks are entered through a form and stored in a local SQLite database. The app also has a Notes page for viewing markdown notes.

## Features

- Add tasks with a name, description, due date, status and priority (0-5)
- Tasks are saved to a SQLite database (`data/tasks.db`, created automatically on first run)
- All saved tasks are shown in a table below the form, filterable by status
- Look up a single task's details by ID
- Notes page renders a markdown note file and lists other note files in `data/Notes/`
- Multipage app (Tasks / Notes) using `st.navigation`

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | App entrypoint: initializes the database and wires up page navigation |
| `pages/task_page.py` | Task form, task table, and task-detail lookup |
| `pages/note_page.py` | Renders a markdown note and lists note files |
| `tools/database.py` | SQLite helpers: creates/updates the table, adds tasks, reads tasks |
| `tools/notes.py` | Lists files in the notes directory |
| `data/` | Holds the SQLite database (`tasks.db`, git-ignored) |
| `data/Notes/` | Markdown note files |
| `docs/notes.md` | Personal setup and learning notes |
| `startup.sh` | Convenience script: activates `.venv` and runs the app (macOS/Linux) |

## Setup

Requires Python 3. The `.venv` folder is git-ignored, so after cloning/pulling on a new machine you must create it yourself and install dependencies again — they don't come with the repo.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install streamlit pandas numpy
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit pandas numpy
```

You'll need to activate the venv (`source .venv/bin/activate` on macOS/Linux, `.venv\Scripts\activate` on Windows) in every new terminal session before running the app.

## Run

Streamlit apps are started with `streamlit run`, not by running the file directly (`python main.py` will fail or do nothing useful):

```bash
streamlit run main.py
```

Then open the URL it prints (usually http://localhost:8501).

On macOS/Linux you can instead run `./startup.sh`, which activates `.venv` and starts the app for you.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'streamlit'`** — the venv isn't created/activated, or dependencies were never installed. Run the Setup steps above.
- **Nothing happens when running `python main.py`** — Streamlit apps must be launched with `streamlit run main.py`, not `python main.py`.

## How the database works

`tools/database.py`'s `init_db()` runs on every start. It creates the `tasks` table if it doesn't exist and adds any columns listed in `COLUMNS` that are missing.

Adding a `CHECK` constraint to an existing column isn't possible with this approach. If you change a constraint, drop the table (or delete `data/tasks.db`) and let the app recreate it.

See [TODO.md](TODO.md) for planned work.
