1. Komunikační vrstva (api_manager.py)
Modul zajišťuje nízkoúrovňové požadavky na API a transformaci dat.
Mapování vstupů: Slovníky GENRE_MAP a PLATFORM_MAP slouží jako translátor mezi uživatelským vstupem (string) a API slugem/ID.
Dynamické parametry: Funkce vyhledej_hry sestavuje objekt params, který určuje filtry pro URL dotaz.

Logika Strict Mode:

Python
```python
if strict and slugy_zanru:
    h_slugs = [z["slug"] for z in h.get("genres", [])]
    if not all(sz in h_slugs for sz in slugy_zanru):
        continue
```
Program využívá list comprehension k extrakci žánrů z každé nalezené hry a funkci all() k ověření kompletní shody se zadáním.

2. Uživatelské rozhraní (menu_pro_uzivatele.py)
Zajišťuje interakci s uživatelem a vizualizaci dat.

Funkce tiskni používá metodu .get() pro přístup k datům ve slovníku. Tím předchází chybám typu KeyError, pokud API vrátí neúplný datový objekt.

Smyčka aplikace: Hlavní menu běží v nekonečném cyklu while True, který je ukončen pouze příkazem (volba 6).

3. Algoritmus náhodného výběru (get_random_game)
Pro dosažení maximální diverzity výsledků je implementována dvoustupňová náhoda:

Náhodná stránka: params["page"] = random.randint(1, 10) – aplikace náhodně volí mezi prvními deseti stránkami výsledků.

Náhodný prvek: random.choice(results) – z vybrané stránky je vybrán jeden konkrétní titul.

4. Vstupní bod (main.py)
Standardní entry point využívající konstrukci if __name__ == "__main__":. Tato implementace umožňuje bezpečný import modulů bez nechtěného spuštění hlavní smyčky menu.
