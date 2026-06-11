import os

SUMMARY_FILE = "summary.txt"

def load_summary():
    if not os.path.exists(SUMMARY_FILE):
        return []

    with open(SUMMARY_FILE, "r", encoding="utf-8") as file:
        return file.readlines()


def save_summary(summary_points):
    with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
        for point in summary_points:
            file.write(point + "\n")


def create_summary(message):

    words = message.split()

    if len(words) > 8:
        return "• " + " ".join(words[:8]) + "..."
    else:
        return "• " + message


def update_summary(message):

    summary = load_summary()

    new_point = create_summary(message)

    summary.append(new_point)

    return [line.strip() for line in summary]