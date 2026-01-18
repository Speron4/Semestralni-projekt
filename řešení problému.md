Neúplná data z API:
Některé starší nebo méně známé hry v databázi RAWG nemají vyplněná všechna pole (např. chybí rok vydání). 
Aby aplikace nespadla při pokusu o výpis, používáme metodu .get() s výchozí hodnotou.
```python
"rok": (h.get("released") or "N/A")[:4],
```
GENRE_MAP:
Místo celého názvu massively-multiplayer stačí zadat krátké mmo.
Před odesláním dotazu aplikace všechny vstupy pomocí .strip().lower() očistí od nechtěných mezer a převede na malá písmena,
čímž eliminuje chyby při zadávání.

Logika u náhodného výběru:
Pokud uživatel u funkce „Šťastný los“ nevyplnil žádné preference (žánr nebo platformu), aplikace by v původní verzi odeslala prázdný dotaz,
což by vedlo k chybě nebo nekonzistentním výsledkům.
ŘEŠENÍ:
Implementace automatického losování výchozích parametrů přímo v kódu funkce `get_random_game`.

```python
# Pokud uživatel nezadá žánr, vylosuje se náhodný z mapy GENRE_MAP
if not genres:
    slugy_zanru = [random.choice(list(GENRE_MAP.values()))]

# Pokud uživatel nezadá platformu, vylosuje se náhodná z PLATFORM_MAP
if not platform:
    p_ids = [random.choice(list(PLATFORM_MAP.values()))]
```
Díky tomuto ošetření aplikace funguje následovně:
Zadání od uživatele: Pokud uživatel napíše "rpg", hledá se náhodná hra v kategorii RPG.
Prázdné zadání: Pokud uživatel jen potvrdí prázdné pole, aplikace se "rozhodne" za něj. Náhodně vybere jeden žánr a jednu platformu z dostupných map a provede dotaz s nimi.
