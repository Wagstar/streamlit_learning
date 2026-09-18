import numpy as np
import streamlit as st
import pandas as pd
from tools import database

database.init_db()

st.write("""
# My first app
Hello *world!*
""")

with st.form("add_task_form",clear_on_submit=True):
    task_name = st.text_input("Task name")
    task_description = st.text_input("Task description")
    due_date = st.text_input("Due date")
    status = st.text_input("Status")
    priority = st.slider("Priority", 0, 5, 0)
    submitted = st.form_submit_button("Submit")
    if submitted:
        if task_name.strip():
            database.add_task(task_name, task_description, due_date, status, priority)
            st.success(f"Task {task_name} added to database")
        else:
            st.error("Task name cannot be empty")
st.subheader("Tasks")
st.dataframe(database.get_tasks())