import requests
from bs4 import BeautifulSoup


def web_search(query):

    try:

        url = f"https://html.duckduckgo.com/html/?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.find_all("a", class_="result__a")

        if not results:
            return "Aucun résultat trouvé."

        text = ""

        for i, result in enumerate(results[:5], start=1):

            title = result.get_text()

            link = "https:" + result["href"]

            text += f"""

{i}. {title}

{link}

"""

        return text

    except Exception as e:

        return f"Erreur web : {str(e)}"
