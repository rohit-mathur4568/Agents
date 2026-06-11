import os

FILE_NAME = "history.txt"

def load_memory():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return file.readlines()


def save_message(role, message):
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(f"{role}: {message}\n")