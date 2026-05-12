from flask import Flask, render_template, request, jsonify
import json
import os
import random
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "data"

CHAT_HISTORY_FILE = f"{DATA_FOLDER}/chat_history.json"
MEMORY_FILE = f"{DATA_FOLDER}/memory.json"

os.makedirs(DATA_FOLDER, exist_ok=True)

for file in [CHAT_HISTORY_FILE, MEMORY_FILE]:

    if not os.path.exists(file):

        with open(file, "w") as f:

            json.dump([], f)


def load_json(path):

    with open(path, "r") as f:

        return json.load(f)


def save_json(path, data):

    with open(path, "w") as f:

        json.dump(data, f, indent=4)


def cloudy_ai(message):

    msg = message.lower()

    greetings = [
        "Salut 😄☁️",
        "Hello humain 🌌",
        "Cloudy est connecté ☁️",
        "Je suis là 😎"
    ]

    if "bonjour" in msg or "salut" in msg:

        return random.choice(greetings)

    if "ça va" in msg:

        return "Toujours dans les nuages 😄☁️"

    if "qui es tu" in msg:

        return "Je suis Cloudy AI, une intelligence artificielle cosmique 🌌"

    if "heure" in msg:

        return f"Il est {datetime.now().strftime('%H:%M:%S')} ⏰"

    if "date" in msg:

        return f"Aujourd'hui : {datetime.now().strftime('%d/%m/%Y')} 📅"

    if "merci" in msg:

        return "Avec plaisir 😄"

    smart_answers = [

        "Intéressant 🤔",
        "Je réfléchis dans le cloud ☁️",
        "Analyse cosmique en cours 🌌",
        "Cloudy traite ta demande 😎",
        "Hmmmm 😄"
    ]

    return random.choice(smart_answers)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message")

    response = cloudy_ai(user_message)

    history = load_json(CHAT_HISTORY_FILE)

    history.append({

        "time": str(datetime.now()),

        "user": user_message,

        "cloudy": response
    })

    save_json(CHAT_HISTORY_FILE, history)

    return jsonify({

        "response": response
    })


if __name__ == "__main__":

    app.run(debug=True)
