import requests
from bs4 import BeautifulSoup

BASE_URL = "https://pkmncards.com/card/mep-{}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_card(code: str):
    url = BASE_URL.format(code)
    resp = requests.get(url, headers=HEADERS, timeout=15)

    if resp.status_code != 200:
        print(f"[ERRO] Não encontrou carta {code} ({resp.status_code})")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Nome da carta
    name_tag = soup.select_one("h1.card-title")
    if not name_tag:
        print(f"[ERRO] Não foi possível localizar o nome da carta {code}")
        return None
    name = name_tag.get_text(strip=True)

    # Dados ficam em uma tabela com class 'card-info'
    data = {}
    table = soup.select_one("table.card-info")
    if table:
        for row in table.select("tr"):
            th = row.select_one("th")
            td = row.select_one("td")
            if th and td:
                data[th.get_text(strip=True)] = td.get_text(strip=True)

    card_info = {
        "code": code,
        "name": name,
        "illustrator": data.get("Illustrator", None),
        "hp": data.get("HP", None),
        "category": data.get("Card Type", None),  # Pokémon Basic, Stage 1...
        "type": data.get("Type", None),
        "number": data.get("Number", None),
    }
    return card_info


def scrape_range(start: int, end: int):
    results = []
    for i in range(start, end + 1):
        code = f"{i:03d}"  # sempre 3 dígitos (004, 005...)
        print(f"Buscando carta {code}...")
        card = scrape_card(code)
        if card:
            results.append(card)
    return results


if __name__ == "__main__":
    # exemplo: 004 até 009
    cartas = scrape_range(4, 9)

    print("\n=== Cartas encontradas ===")
    for c in cartas:
        print(c)
