import streamlit as st
from tools import database

database.init_db()

pg = st.navigation([
    st.Page("pages/task_page.py", title="Task Page")
])
pg.run()

