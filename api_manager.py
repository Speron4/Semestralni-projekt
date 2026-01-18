import requests
import random

# Konstanty zůstávají stejné
GENRE_MAP = {
    "rpg": "role-playing-games-rpg", "akcni": "action", "action": "action",
    "indie": "indie", "dobrodruzne": "adventure", "adventure": "adventure",
    "strilecka": "shooter", "shooter": "shooter", "strategie": "strategy",
    "strategy": "strategy", "casual": "casual", "simulace": "simulation",
    "simulation": "simulation", "logicke": "puzzle", "puzzle": "puzzle",
    "arkada": "arcade", "arcade": "arcade", "skakacka": "platformer",
    "platformer": "platformer", "zavodni": "racing", "racing": "racing",
    "mmo": "massively-multiplayer", "sportovni": "sports", "sports": "sports",
    "bojove": "fighting", "fighting": "fighting", "rodinne": "family",
    "family": "family", "deskovky": "board-games", "vdelavaci": "educational",
    "karetni": "card"
}

PLATFORM_MAP = {
    "pc": "4", "ps5": "187", "ps4": "18", "ps3": "16", "ps2": "15",
    "xbox-series": "186", "xbox-one": "1", "switch": "7"
}


def _get_api_key():
    """Pomocná funkce pro načtení API klíče."""
    try:
        with open("api.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def _formatuj_hru(h):
    """Sjednotí formátování dat o hře z API odpovědi."""
    return {
        "jmeno": h.get("name"),
        "rok": (h.get("released") or "N/A")[:4],
        "rating": h.get("rating", 0),
        "zanry": [z["name"] for z in h.get("genres", [])],
        "platformy": [p["platform"]["name"] for p in h.get("platforms", [])],
        "slug": h.get("slug")
    }


def vyhledej_hry(genres="", platforms="", strict=False):
    klic = _get_api_key()
    if not klic: return []

    # Vyčištění vstupů od mezer
    vstupy_zanry = [z.strip().lower() for z in genres.split(",")] if genres else []
    slugy_zanru = [GENRE_MAP.get(z, z) for z in vstupy_zanry if z]

    p_vstupy = [p.strip().lower() for p in platforms.split(",")] if platforms else []
    p_ids = [PLATFORM_MAP[p] for p in p_vstupy if p in PLATFORM_MAP]

    params = {
        "key": klic,
        "page_size": 100 if strict else 40,
    }

    # Přidáme parametry jen pokud nejsou prázdné
    if slugy_zanru:
        params["genres"] = ",".join(slugy_zanru)
    if p_ids:
        params["platforms"] = ",".join(p_ids)

    try:
        res = requests.get("https://api.rawg.io/api/games", params=params, timeout=10).json()
        hry = []
        results = res.get("results", [])

        for h in results:
            if strict and slugy_zanru:
                h_slugs = [z["slug"] for z in h.get("genres", [])]
                # Musí obsahovat všechny hledané žánry
                if not all(sz in h_slugs for sz in slugy_zanru):
                    continue
            hry.append(_formatuj_hru(h))
        return hry
    except Exception as e:
        print(f"Chyba při komunikaci s API: {e}")
        return []


def get_top_10_by_year(year):
    klic = _get_api_key()
    if not klic: return []

    params = {
        "key": klic,
        "dates": f"{year}-01-01,{year}-12-31",
        "ordering": "-rating",
        "page_size": 10
    }

    try:
        res = requests.get("https://api.rawg.io/api/games", params=params, timeout=10).json()
        return [_formatuj_hru(h) for h in res.get("results", [])]
    except:
        return []


def get_random_game(genres="", platform="", year=""):
    klic = _get_api_key()
    if not klic: return None

    # Zpracování žánrů - pokud uživatel nezadá nic, vylosuje se náhodný z GENRE_MAP
    if genres:
        vstupy_zanry = [z.strip().lower() for z in genres.split(",")]
        slugy_zanru = [GENRE_MAP.get(z, z) for z in vstupy_zanry if z]
    else:
        # Losování náhodného žánru z hodnot v mapě
        slugy_zanru = [random.choice(list(GENRE_MAP.values()))]

    # Zpracování platforem - pokud uživatel nezadá nic, vylosuje se náhodná z PLATFORM_MAP
    if platform:
        vstupy_platforem = [p.strip().lower() for p in platform.split(",")]
        p_ids = [str(PLATFORM_MAP[p]) for p in vstupy_platforem if p in PLATFORM_MAP]
    else:
        # Losování náhodné platformy z hodnot v mapě
        p_ids = [random.choice(list(PLATFORM_MAP.values()))]

    params = {
        "key": klic,
        "page_size": 40,
        "genres": ",".join(slugy_zanru),
        "platforms": ",".join(p_ids)
    }

    try:
        # Přidáme náhodnou stránku pro větší variabilitu výsledků
        params["page"] = random.randint(1, 10)

        res = requests.get("https://api.rawg.io/api/games", params=params, timeout=10).json()
        results = res.get("results", [])

        # Pokud je náhodná stránka prázdná, zkusíme první
        if not results:
            params["page"] = 1
            res = requests.get("https://api.rawg.io/api/games", params=params, timeout=10).json()
            results = res.get("results", [])

        return _formatuj_hru(random.choice(results)) if results else None
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
