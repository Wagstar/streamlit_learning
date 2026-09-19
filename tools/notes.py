import os

directory_path = "data/Notes/"

def get_note_files():
    try:
        files = os.listdir(directory_path)
        return [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
        return []
