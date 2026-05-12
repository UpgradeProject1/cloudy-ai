def detect_language(message):

    french_words = [
        "bonjour",
        "salut",
        "comment",
        "merci",
        "oui"
    ]

    english_words = [
        "hello",
        "hi",
        "how",
        "thanks",
        "yes"
    ]

    message = message.lower()

    french_score = 0
    english_score = 0

    for word in french_words:
        if word in message:
            french_score += 1

    for word in english_words:
        if word in message:
            english_score += 1

    if english_score > french_score:
        return "english"

    return "french"


def ask_ai(message):

    language = detect_language(message)

    msg = message.lower()

    if language == "french":

        if "bonjour" in msg or "salut" in msg:
            return "Salut 👋"

        if "comment ça va" in msg:
            return "Je vais bien 😄"

        if "ton nom" in msg:
            return "Je suis Cloudy AI ☁️"

        return "Je parle français 🇫🇷"

    else:

        if "hello" in msg or "hi" in msg:
            return "Hello 👋"

        if "how are you" in msg:
            return "I'm doing great 😄"

        if "your name" in msg:
            return "I am Cloudy AI ☁️"

        return "I speak English 🇬🇧"
