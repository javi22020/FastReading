import os

def choose_from_folder(folder: str):
    list_files = os.listdir(folder)
    if len(list_files) == 1:
        return folder + list_files[0]
    else:
        pass