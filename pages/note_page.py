import streamlit as st
from pathlib import Path
from tools import notes

PATH_TO_NOTES = "/Users/uypetter/Python/streamlit_learning/data/Notes/TestNote.md"

markdowncontent = Path(PATH_TO_NOTES).read_text()
st.markdown(markdowncontent, unsafe_allow_html=True)

text_files = notes.get_note_files()
st.text(f"Text files in {notes.directory_path}: {text_files}")
st.text(f"text file is variable is of type: {type(text_files)}")
