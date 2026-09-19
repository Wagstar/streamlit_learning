import streamlit as st
from tools import database

st.title("Task Manager")
st.header("Tasks Manager")
st.text("Input your task below")

with st.form("Add_task_form", clear_on_submit=True):
    task_name = st.text_input("Task name")
    task_description = st.text_input("Task description")
    due_date = st.date_input("Due date")
    priority = st.slider("Priority", 0, 5, 0)
    submitted = st.form_submit_button("Add task")

    if submitted:
        if task_name.strip():
            database.add_task(task_name, task_description, due_date, priority)
            st.success(f"Task {task_name} added successfully")
        else:
            st.error("Please enter a valid task")

st.subheader("Tasks")
st.show_only = st.selectbox(
    "Status",
    ("All", "Active", "Completed", "Pending", "On Hold", "Canceled")
)
if st.show_only != "All":
    st.dataframe(database.get_tasks().query("status == @st.show_only"))
else:
    st.dataframe(database.get_tasks())


