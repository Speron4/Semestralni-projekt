import requests
import random

# Překladová mapa pro všechny žánry na RAWG
# Klíč je to, co napíše uživatel, hodnota je to, co chce server
GENRE_MAP = {
    "rpg": "role-playing-games-rpg",
    "akcni": "action", "action": "action",
    "indie": "indie",
    "dobrodruzne": "adventure", "adventure": "adventure",
    "strilecka": "shooter", "shooter": "shooter",
    "strategie": "strategy", "strategy": "strategy",
    "casual": "casual",
    "simulace": "simulation", "simulation": "simulation",
    "logicke": "puzzle", "puzzle": "puzzle",
    "arkada": "arcade", "arcade": "arcade",
    "skakacka": "platformer", "platformer": "platformer",
    "zavodni": "racing", "racing": "racing",
    "mmo": "massively-multiplayer",
    "sportovni": "sports", "sports": "sports",
    "bojove": "fighting", "fighting": "fighting",
    "rodinne": "family", "family": "family",
    "deskovky": "board-games",
    "vdelavaci": "educational",
    "karetni": "card"
}

PLATFORM_MAP = {
    "pc": "4", "ps5": "187", "ps4": "18", "ps3": "16", "ps2": "15",
    "xbox-series": "186", "xbox-one": "1", "switch": "7"
}


def get_random_game(genres="", platform="", year=""):
    try:
        with open("api.txt", "r") as f:
            klic = f.read().strip()
    except:
        return None

    # Sestavení URL pro náhodný výběr
    url = f"https://api.rawg.io/api/games?key={klic}&page_size=40"

    if platform in PLATFORM_MAP:
        url += f"&platforms={PLATFORM_MAP[platform]}"
    if genres:
        url += f"&genres={genres.lower().replace(' ', '')}"
    if year:
        url += f"&dates={year}-01-01,{year}-12-31"

    try:
        res = requests.get(url, timeout=10).json()
        results = res.get("results", [])

        if not results:
            return None

        # Výběr náhodné hry ze seznamu
        h = random.choice(results)
        return {
            "jmeno": h.get("name"),
            "rok": h.get("released")[:4] if h.get("released") else "N/A",
            "rating": h.get("rating", 0),
            "zanry": [z["name"] for z in h.get("genres", [])],
            "platformy": [p["platform"]["name"] for p in h.get("platforms", [])]
        }
    except:
        return None

def get_top_10_by_year(year):
    try:
        with open("api.txt", "r", encoding="utf-8") as f:
            klic = f.read().strip()
    except:
        return []

    url = "https://api.rawg.io/api/games"
    # dates=YYYY-01-01,YYYY-12-31 vyfiltruje hry jen pro dany rok
    # ordering=-rating zajisti, ze nejlepsi hry budou na zacatku
    params = {
        "key": klic,
        "dates": f"{year}-01-01,{year}-12-31",
        "ordering": "-rating",
        "page_size": 10
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        vysledky = []

        for game in data.get("results", []):
            vysledky.append({
                "jmeno": game.get("name"),
                "rok": year,
                "rating": game.get("rating", 0),
                "zanry": [z["name"] for z in game.get("genres", [])],
                "platformy": [p["platform"]["name"] for p in game.get("platforms", [])]
            })
        return vysledky
    except:
        return []


def vyhledej_hry(genres="", platforms="", strict=False):
    try:
        with open("api.txt", "r") as f:
            klic = f.read().strip()
    except:
        return []

    p_ids = []
    # Rozdeleni platform pro filtraci
    v_platf = [p.strip().lower() for p in platforms.split(",")] if platforms else []
    for p in v_platf:
        if p in PLATFORM_MAP:
            p_ids.append(PLATFORM_MAP[p])

    # Zakladni URL (pokud je strict, chceme vetsi vzorek dat pro filtraci)
    limit = 100 if strict else 40
    url = f"https://api.rawg.io/api/games?key={klic}&page_size={limit}"

    if p_ids: url += f"&platforms={','.join(p_ids)}"
    if genres: url += f"&genres={genres.lower().replace(' ', '')}"

    try:
        res = requests.get(url, timeout=10).json()
        hry = []
        # Rozdeleni zadanych zanru pro kontrolu
        v_zanry = [z.strip().lower() for z in genres.split(",")] if (genres and strict) else []

        for h in res.get("results", []):
            h_slug_z = [z["slug"] for z in h.get("genres", [])]

            if strict:
                # Kontrola: Musi mit VSECHNY zadane zanry najednou
                # Hledame, zda je kazdy vyzadovany zanr obsazen v tech od API
                if not all(any(vz in hz for hz in h_slug_z) for vz in v_zanry):
                    continue

            hry.append({
                "jmeno": h.get("name"),
                "rok": h.get("released")[:4] if h.get("released") else "N/A",
                "rating": h.get("rating", 0),
                "zanry": [z["name"] for z in h.get("genres", [])],
                "platformy": [p["platform"]["name"] for p in h.get("platforms", [])]
            })
        return hry
    except:
        return []


def get_top_10_by_year(year):
    try:
        with open("api.txt", "r") as f:
            klic = f.read().strip()
        url = f"https://api.rawg.io/api/games?key={klic}&dates={year}-01-01,{year}-12-31&ordering=-rating&page_size=10"
        res = requests.get(url, timeout=10).json()
        return [{
            "jmeno": h.get("name"),
            "rok": year,
            "rating": h.get("rating", 0),
            "zanry": [z["name"] for z in h.get("genres", [])],
            "platformy": [p["platform"]["name"] for p in h.get("platforms", [])]
        } for h in res.get("results", [])]
    except:
        return []






# Příklad volání:
# data = fetch_all_games_from_api()



""""Test zda vše funguje správně
from datetime import datetime

if __name__ == "__main__":
    hry = fetch_data_from_api(pages=3)
    print("Ukázka prvních 3 her:")

    for hra in hry[:3]:
        datum = hra["Datum_vydani"]

        # Zkontroluje, jestli existuje datum
        if datum:
            # Převod z formátu "YYYY-MM-DD" → "DD. MM. YYYY"
            datum_objekt = datetime.strptime(datum, "%Y-%m-%d")
            datum_format = datum_objekt.strftime("%d. %m. %Y")
        else:
            datum_format = "Neznámé datum"

        print(f"- {hra['Jmeno']} ({datum_format})")
"""