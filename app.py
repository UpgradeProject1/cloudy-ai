from flask import Flask, render_template, request, jsonify
import json
import os
import random
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "data"

CHAT_HISTORY_FILE = f"{DATA_FOLDER}/chat_history.json"

os.makedirs(DATA_FOLDER, exist_ok=True)

if not os.path.exists(CHAT_HISTORY_FILE):

    with open(CHAT_HISTORY_FILE, "w") as f:

        json.dump([], f)


def load_history():

    with open(CHAT_HISTORY_FILE, "r") as f:

        return json.load(f)


def save_history(history):

    with open(CHAT_HISTORY_FILE, "w") as f:

        json.dump(history, f, indent=4)


def cloudy_ai(message):

    msg = message.lower()

    greetings = [

        "Salut 😄☁️",

        "Hello 🌌",

        "Cloudy est là ☁️",

        "Yo 😎"
    ]

    if "bonjour" in msg or "salut" in msg:

        return random.choice(greetings)

    if "ça va" in msg:

        return "Toujours dans les nuages ☁️"

    if "heure" in msg:

        return f"Il est {datetime.now().strftime('%H:%M:%S')} ⏰"

    if "date" in msg:

        return f"Aujourd'hui : {datetime.now().strftime('%d/%m/%Y')} 📅"

    if "merci" in msg:

        return "Avec plaisir 😄"

    smart_answers = [

        "Analyse cosmique en cours 🌌",

        "Cloudy réfléchit ☁️",

        "Hmmmm 😄",

        "Intéressant 🤔"
    ]

    return random.choice(smart_answers)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    response = cloudy_ai(user_message)

    history = load_history()

    history.append({

        "time": str(datetime.now()),

        "user": user_message,

        "cloudy": response
    })

    save_history(history)

    return jsonify({

        "response": response
    })


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
