# Todo

- [ ] Add UI to edit/delete a task (`update_task` and `delete_task` already exist in `tools/database.py` but nothing in the app calls them yet)
- [ ] Make `tools/notes.py`'s `directory_path` resolve relative to the project root like `tools/database.py` does, instead of relying on Streamlit's working directory
- [ ] Let the Notes page pick which note file to view, instead of always showing the hardcoded `TestNote.md`
- [ ] Add a `requirements.txt` so `pip install streamlit pandas numpy` isn't duplicated by hand from the README
- [ ] Add a Windows equivalent of `startup.sh`
- [ ] Add a `Dockerfile` (and `docker-compose.yml` with a volume mount for `data/`) so the app can run in Docker
