import os

SUMMARY_FILE = "summary.txt"


def load_summary():

    if not os.path.exists(SUMMARY_FILE):
        return ""

    with open(SUMMARY_FILE, "r", encoding="utf-8") as file:
        return file.read()


def save_summary(summary):

    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
        file.write(summary)


def update_summary(old_summary, user_message):

    if old_summary == "":
        return user_message

    return old_summary + "\n" + user_message