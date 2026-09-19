import streamlit as st
from tools import database

st.title("Task Manager")
st.header("Task Manager")
st.text("Input your tasks below and manage them easily.")

with st.form("add_task_form",clear_on_submit=True):
    # Task name field
    task_name = st.text_input("Task name")

    # Task description field
    task_description = st.text_input("Task description")

    # Due date field, gets data from streamlit date_input, which returns a datetime.date object.
    # We convert it to ISO format string for storage in the database.
    due_date = st.date_input("Due date")

    # Status field, using a selectbox for predefined options
    status = st.selectbox(
        "Status",
        ("Active", "Completed", "Pending", "On Hold", "Cancelled"),
    )
    # Display the selected status below the selectbox
    st.text(f"Status: {status}")

    # Priority field, using a slider for integer values between 0 and 5
    priority = st.slider("Priority", 0, 5, 0)

    # Submit button for the form
    submitted = st.form_submit_button("Submit")

    # If the form is submitted, add the task to the database. The add mechanic
    if submitted:
        if task_name.strip():
            database.add_task(task_name, task_description, due_date.isoformat(), str(status), priority)
            st.success(f"Task {task_name} added to database")
        else:
            st.error("Task name cannot be empty")

st.subheader("Tasks")
st.showOnly = st.selectbox(
    "Status",
    ("All", "Active", "Completed", "Pending", "On Hold", "Cancelled"),
)
if st.showOnly != "All":
    st.dataframe(database.get_tasks().query("status == @st.showOnly"))
else:
    st.dataframe(database.get_tasks())

st.subheader("Read details of a task")
task_id = st.number_input("Task ID to read details", min_value=1, step=1)
st.text(f"Details for task ID {task_id}:")
task_details = database.get_tasks().query("id == @task_id")
if not task_details.empty:
    st.json(task_details.to_dict(orient="records")[0])
else:
    st.warning(f"No task found with ID {task_id}")
