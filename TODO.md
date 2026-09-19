# TODO

## New pages

- [ ] Finish `note_page` (in progress)
- [ ] Calendar page
- [ ] Dashboard page
- [ ] Daily page

### Idea: merge Dashboard + Daily, module-based

Still just brainstorming, not decided. Daily page and Home Dashboard might end up being the same page rather than two separate ones, since a "what's next" summary is inherently daily-scoped anyway.

Rough shape:
- A "what's next" summary module (upcoming/overdue tasks).
- A clickable list of notes that jumps into `note_page` for that note.
- Built as small, self-contained modules (e.g. a task-summary module, a notes-list module) composed on one page, rather than one monolithic page — keeps the page thin and lets a module (like task-summary) be reused elsewhere later.

Open question: if Daily later needs to be date-scoped (navigate back/forward through past or future days, like a journal), that's a different interaction model than a dashboard that always shows "right now" — might be worth splitting back out at that point.

## Editable task table (data_editor)

Replace the read-only `st.dataframe` task table in `pages/task_page.py` with an editable grid, so tasks can be updated directly instead of only being added.

**Approach:** swap `st.dataframe(...)` for `st.data_editor(...)`, then diff the edited DataFrame against the original on a "Save changes" button and push only the changed cells to the DB via the existing `update_task` / `set_task_completed` helpers in `tools/database.py`.

### Implementation guide

1. Fetch the current tasks into a DataFrame before rendering the editor, and keep that as your "original" reference:
   ```python
   original_df = database.get_tasks()
   ```

2. Render it with `st.data_editor` instead of `st.dataframe`:
   - Mark columns that should never be hand-edited as read-only via `disabled=[...]` — at minimum `id`, `created_timestamp`, `completed_timestamp`.
   - Constrain editable columns with `column_config` so users can't enter values that violate the DB's `CHECK` constraints:
     - `status` -> `st.column_config.SelectboxColumn(options=["Pending", "Active", "On Hold", "Completed"])`
     - `priority` -> `st.column_config.NumberColumn(min_value=0, max_value=5, step=1)`
     - `due_date` -> `st.column_config.DateColumn()`
   ```python
   edited_df = st.data_editor(
       original_df,
       key="task_editor",
       disabled=["id", "created_timestamp", "completed_timestamp"],
       column_config={
           "status": st.column_config.SelectboxColumn(options=["Pending", "Active", "On Hold", "Completed"]),
           "priority": st.column_config.NumberColumn(min_value=0, max_value=5, step=1),
           "due_date": st.column_config.DateColumn(),
       },
       hide_index=True,
   )
   ```

3. On a "Save changes" button, diff `edited_df` against `original_df` (e.g. `edited_df.compare(original_df)`) to find which rows/columns actually changed, then for each changed cell:
   - If the column is `status` and the new value is `"Completed"`, call `database.set_task_completed(task_id)` instead of a plain update, so `completed_timestamp` gets stamped too.
   - Otherwise call `database.update_task(task_id, column, new_value)`.
   ```python
   if st.button("Save changes"):
       changes = edited_df.compare(original_df)
       for row_id in changes.index:
           task_id = int(original_df.loc[row_id, "id"])
           for column in changes.columns.get_level_values(0).unique():
               new_value = edited_df.loc[row_id, column]
               if column == "status" and new_value == "Completed":
                   database.set_task_completed(task_id)
               else:
                   database.update_task(task_id, column, new_value)
       st.success("Saved")
       st.rerun()
   ```

### Watch out for

- `df.compare()` needs matching indexes/dtypes between `original_df` and `edited_df` — `data_editor` preserves the index by default, but dtype mismatches (e.g. `priority` as `int64` vs `float64` if there are `NaN`s) can break the diff.
- Streamlit reruns the whole script on every interaction, so make sure `original_df` reflects the last *saved* state, not a half-edited in-progress state from a prior rerun.
- No per-row confirmation/undo — "Save changes" commits every changed row in the grid at once. Fine for quick triage, but there's no "are you sure" step.
- `set_task_completed` in `tools/database.py` currently has a SQL bug (`UPDATE ... SET (...) VALUES (...)` isn't valid syntax) — needs fixing before this can actually be wired up to it.

### Alternative considered

Instead of a whole-grid editor, a "select one task, edit via a form" flow was also considered — more deliberate (good spot for a "Mark Complete" / delete button per task), but adds an extra selection step versus editing inline. Went with `data_editor` first since it reuses `update_task` cleanly for bulk/quick edits.
