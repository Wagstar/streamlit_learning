import streamlit as st
from tools import database

database.init_db()

pg = st.navigation([
    st.Page("pages/task_page.py", title="Tasks", icon="📝"),
    st.Page("pages/note_page.py", title="Notes", icon="🗒️"),
])
pg.run()
