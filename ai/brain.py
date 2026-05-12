import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3"


def ask_nova_stream(message):

    prompt = f"""
You are Cloudy, a futuristic AI assistant.

IMPORTANT:
- Reply in the SAME language as the user.
- Be natural and intelligent.
- Be friendly and modern.
- Keep answers clean and readable.

User:
{message}

Cloudy:
"""

    response = requests.post(

        OLLAMA_URL,

        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True
        },

        stream=True
    )

    for line in response.iter_lines():

        if line:

            data = json.loads(line)

            if "response" in data:

                yield data["response"]
