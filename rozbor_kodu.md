1. Komunikační vrstva (api_manager.py)
   
Modul zajišťuje nízkoúrovňové požadavky na API a transformaci dat.
Mapování vstupů: Slovníky GENRE_MAP a PLATFORM_MAP slouží jako překladatel mezi uživatelským vstupem (string) a API slugem/ID.
Dynamické parametry: Funkce vyhledej_hry sestavuje objekt params, který určuje filtry pro URL dotaz.

.join(): Tato metoda je klíčová. Umožňuje uživateli zadat seznam (např. ["action", "rpg"]) a automaticky ho převede na formát action,rpg, který vyžaduje API.

page_size: Nastavením této hodnoty omezujeme množství přenesených dat, což zrychluje odezvu aplikace.

Data, která přijdou z API, jsou obrovské vnořené struktury (JSON). Funkce _formatuj_hru slouží jako filtr, který vytáhne jen to, co nás zajímá.

```python
def _formatuj_hru(h):
    return {
        "jmeno": h.get("name"),
        "rok": (h.get("released") or "N/A")[:4],
        "rating": h.get("rating", 0),
        # ...
    }
```
List Comprehension: 
Rychle vytvoří seznam slugů žánrů pro každou konkrétní hru.
all(): Tato vestavěná funkce Pythonu zkontroluje, zda jsou všechny hledané žánry přítomny v seznamu žánrů dané hry. Pokud ne, continue hru přeskočí a nepřidá ji do výsledků.


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
