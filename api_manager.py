import requests
import random

# Překladová mapa pro žánry na RAWG
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

def vyhledej_hry(genres="", platforms="", strict=False):
    try:
        with open("api.txt", "r") as f:
            klic = f.read().strip()
    except:
        return []

    # Překlad žánrů přes GENRE_MAP
    seznam_vstupu = [z.strip().lower() for z in genres.split(",")] if genres else []
    opravene_zanry = [GENRE_MAP.get(z, z) for z in seznam_vstupu]
    final_genres = ",".join(opravene_zanry)

    p_ids = [PLATFORM_MAP[p.strip().lower()] for p in platforms.split(",") if p.strip().lower() in PLATFORM_MAP]
    
    limit = 100 if strict else 40
    url = f"https://api.rawg.io/api/games?key={klic}&page_size={limit}"
    if p_ids: url += f"&platforms={','.join(p_ids)}"
    if final_genres: url += f"&genres={final_genres}"

    try:
        res = requests.get(url, timeout=10).json()
        hry = []
        for h in res.get("results", []):
            h_slug_z = [z["slug"] for z in h.get("genres", [])]
            if strict and genres:
                if not all(any(vz in hz for hz in h_slug_z) for vz in opravene_zanry):
                    continue
            hry.append({
                "jmeno": h.get("name"),
                "rok": h.get("released")[:4] if h.get("released") else "N/A",
                "rating": h.get("rating", 0),
                "zanry": [z["name"] for z in h.get("genres", [])],
                "platformy": [p["platform"]["name"] for p in h.get("platforms", [])],
                "slug": h.get("slug")
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
            "jmeno": h.get("name"), "rok": year, "rating": h.get("rating", 0),
            "zanry": [z["name"] for z in h.get("genres", [])],
            "platformy": [p["platform"]["name"] for p in h.get("platforms", [])],
            "slug": h.get("slug")
        } for h in res.get("results", [])]
    except:
        return []

def get_random_game(genres="", platform="", year=""):
    try:
        with open("api.txt", "r") as f:
            klic = f.read().strip()
    except:
        return None
    
    # Překlad žánrů i pro náhodný výběr
    seznam_vstupu = [z.strip().lower() for z in genres.split(",")] if genres else []
    opravene_zanry = [GENRE_MAP.get(z, z) for z in seznam_vstupu]
    final_genres = ",".join(opravene_zanry)

    url = f"https://api.rawg.io/api/games?key={klic}&page_size=40"
    if platform in PLATFORM_MAP: url += f"&platforms={PLATFORM_MAP[platform]}"
    if final_genres: url += f"&genres={final_genres}"
    if year: url += f"&dates={year}-01-01,{year}-12-31"

    try:
        res = requests.get(url, timeout=10).json()
        results = res.get("results", [])
        if not results: return None
        h = random.choice(results)
        return {
            "jmeno": h.get("name"),
            "rok": h.get("released")[:4] if h.get("released") else "N/A",
            "rating": h.get("rating", 0),
            "zanry": [z["name"] for z in h.get("genres", [])],
            "platformy": [p["platform"]["name"] for p in h.get("platforms", [])],
            "slug": h.get("slug")
        }
    except:
        return None






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

