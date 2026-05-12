import subprocess
import json
import os

NOTES_FILE = "data/notes.json"
TODO_FILE = "data/todos.json"


def load_notes():

    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r") as file:

        try:
            return json.load(file)

        except:
            return []


def save_notes(notes):

    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)


def load_todos():

    if not os.path.exists(TODO_FILE):
        return []

    with open(TODO_FILE, "r") as file:

        try:
            return json.load(file)

        except:
            return []


def save_todos(todos):

    with open(TODO_FILE, "w") as file:
        json.dump(todos, file, indent=4)


def run_command(message):

    message = message.lower()

    if "/files" in message:

        subprocess.Popen(["xdg-open", "."])

        return "Gestionnaire de fichiers ouvert."

    if "/home" in message:

        subprocess.Popen(["xdg-open", "/home/frank"])

        return "Dossier home ouvert."

    if message.startswith("/note "):

        note = message.replace("/note ", "")

        notes = load_notes()

        notes.append(note)

        save_notes(notes)

        return f"Note ajoutée : {note}"

    if message.strip() == "/notes":

        notes = load_notes()

        if not notes:
            return "Aucune note."

        result = "Notes NOVA :\n\n"

        for i, note in enumerate(notes, start=1):

            result += f"{i}. {note}\n"

        return result

    if message.startswith("/todo "):

        task = message.replace("/todo ", "")

        todos = load_todos()

        todos.append(task)

        save_todos(todos)

        return f"Tâche ajoutée : {task}"

    if message.strip() == "/todos":

        todos = load_todos()

        if not todos:
            return "Aucune tâche."

        result = "Tâches NOVA :\n\n"

        for i, task in enumerate(todos, start=1):

            result += f"{i}. {task}\n"

        return result

    if message.startswith("/done "):

        try:

            index = int(message.replace("/done ", "")) - 1

            todos = load_todos()

            removed = todos.pop(index)

            save_todos(todos)

            return f"Tâche terminée : {removed}"

        except:

            return "Numéro invalide."

    return None
