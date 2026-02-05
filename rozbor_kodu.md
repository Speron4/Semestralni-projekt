`api manager`
Tato funkce slouží k bezpečnému získání přístupového klíče:
Používá blok `try-except` pro ošetření chyby `FileNotFoundError`. Pokud soubor api.txt neexistuje, funkce nezhodí celou aplikaci, ale vrátí `None`.
```python
def _get_api_key():
    try:
        with open("api.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
```
---
`_formatuj_hru(h)`
Pomocná funkce, která transformuje rozsáhlý a nepřehledný objekt z API na jednoduchý a čitelný slovník.
Metoda `.get()` zajišťuje, že pokud nějaký údaj v databázi chybí, aplikace nespadne.
```python
def _formatuj_hru(h):
    return {
        "jmeno": h.get("name"),
        "rok": (h.get("released") or "N/A")[:4],
        "rating": h.get("rating", 0),
        "zanry": [z["name"] for z in h.get("genres", [])],
        "platformy": [p["platform"]["name"] for p in h.get("platforms", [])],
        "slug": h.get("slug")
    }
```
---
`vyhledej_hry()`
Sestavuje HTTP požadavky a implementuje pokročilé filtrování.
Převádí uživatelský text na seznam slugů pomocí `GENRE_MAP`.
Pomocí cyklu a funkce `all()` jsem do aplikace přidal možnost striktního vyhledávání, kdy hra musí splňovat všechna kritéria najednou.
```python
def vyhledej_hry(genres="", platforms="", strict=False):
    klic = _get_api_key()
    if not klic: return []

    vstupy_zanry = [z.strip().lower() for z in genres.split(",")] if genres else []
    slugy_zanru = [GENRE_MAP.get(z, z) for z in vstupy_zanry if z]
    
    # ... sestavení params a requests.get ...

    for h in results:
        if strict and slugy_zanru:
            h_slugs = [z["slug"] for z in h.get("genres", [])]
            if not all(sz in h_slugs for sz in slugy_zanru):
                continue
        hry.append(_formatuj_hru(h))
    return hry
```
`get_top_10_by_year(year)`
Funkce specializovaná na získání dat pro konkrétní rok.
Používá parametr dates pro vymezení celého kalendářního roku.
Parametr ordering: `"-rating"` říká API, aby výsledky seřadilo sestupně od nejlépe hodnocených po nejhorší.
```python
def get_top_10_by_year(year):
    params = {
        "key": klic,
        "dates": f"{year}-01-01,{year}-12-31",
        "ordering": "-rating",
        "page_size": 10
    }
```
---
`get_random_game()`
Zajišťuje funkci "Šťastný los" s vysokou mírou variability.
Prvně se náhodně zvolí jedna z deseti stránek výsledků (`random.randint`) a následně jedna konkrétní hra z této stránky (`random.choice`).
```python
def get_random_game(genres="", platform="", year=""):
    # ... fallback logika pro prázdné vstupy ...
    try:
        params["page"] = random.randint(1, 10)
        res = requests.get("https://api.rawg.io/api/games", params=params, timeout=10).json()
        results = res.get("results", [])

        if not results:
            params["page"] = 1
            # ... opakovaný dotaz ...
        return _formatuj_hru(random.choice(results))
    except:
        return None
```
---
`menu_pro_uzivatele.py`

Zajišťuje interakci s uživatelem a čitelný výstup do terminálu.

`tiskni(vysledky)`: Formátuje surová data z API do přehledných bloků. Používá metodu `.get()`, aby program nespadl při chybějících údajích (např. u chybějícího roku vydání).

menu(): Hlavní ovládací prvek aplikace. Běží v nekonečné smyčce while True, která umožňuje opakované hledání bez restartu programu. Ukončuje se pouze volbou "6" (break).
---
`main.py`
Slouží jako spouštěč.
```python
from menu_pro_uzivatele import menu

def main():
    menu()

if __name__ == "__main__":
    main()
```

