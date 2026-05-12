from flask import Flask, render_template, request, jsonify, Response
from ai.brain import ask_nova_stream
import json
import os
import uuid

app = Flask(__name__)

NOTES_FILE = "data/notes.json"
TODO_FILE = "data/todos.json"

CONVERSATIONS_FOLDER = "data/conversations"


def load_json(file):

    if not os.path.exists(file):
        return []

    with open(file, "r") as f:

        try:
            return json.load(f)

        except:
            return []


def save_json(file, data):

    with open(file, "w") as f:

        json.dump(data, f, indent=4)


def get_conversations():

    conversations = []

    for file in os.listdir(CONVERSATIONS_FOLDER):

        if file.endswith(".json"):

            path = os.path.join(
                CONVERSATIONS_FOLDER,
                file
            )

            data = load_json(path)

            title = "Nouvelle conversation"

            if len(data) > 0:

                title = data[0]["user"][:30]

            conversations.append({
                "id": file.replace(".json", ""),
                "title": title
            })

    return conversations


@app.route("/")
def home():

    notes = load_json(NOTES_FILE)

    todos = load_json(TODO_FILE)

    conversations = get_conversations()

    return render_template(
        "index.html",
        notes=notes,
        todos=todos,
        conversations=conversations
    )


@app.route("/new_chat")
def new_chat():

    chat_id = str(uuid.uuid4())

    save_json(
        f"{CONVERSATIONS_FOLDER}/{chat_id}.json",
        []
    )

    return jsonify({
        "chat_id": chat_id
    })


@app.route("/load_chat/<chat_id>")
def load_chat(chat_id):

    path = f"{CONVERSATIONS_FOLDER}/{chat_id}.json"

    history = load_json(path)

    return jsonify(history)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data["message"]

    chat_id = data["chat_id"]

    path = f"{CONVERSATIONS_FOLDER}/{chat_id}.json"

    history = load_json(path)

    def generate():

        full_response = ""

        for chunk in ask_nova_stream(message):

            full_response += chunk

            yield chunk

        history.append({
            "user": message,
            "nova": full_response
        })

        save_json(path, history)

    return Response(generate(), mimetype="text/plain")


@app.route("/delete_chat/<chat_id>")
def delete_chat(chat_id):

    path = f"{CONVERSATIONS_FOLDER}/{chat_id}.json"

    if os.path.exists(path):

        os.remove(path)

    return "deleted"


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
