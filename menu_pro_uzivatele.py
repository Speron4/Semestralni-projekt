from api_manager import vyhledej_hry, get_top_10_by_year, get_random_game


def tiskni(vysledky, specialni_text=None):
    if not vysledky:
        print("\n--- Zadna hra neodpovida zadani ---")
        return

    # Pokud je výsledkem jedna hra (slovník), uděláme z ní seznam
    if isinstance(vysledky, dict):
        vysledky = [vysledky]

    # Vypíšeme buď speciální text, nebo počet nalezených her
    if specialni_text:
        print(f"\n{specialni_text}")
    else:
        print(f"\nNalezeno {len(vysledky)} her:")

    for h in vysledky:
        if not isinstance(h, dict):
            continue

        print(f"-> {h.get('jmeno', 'Neznámý název').upper()} ({h.get('rok', 'N/A')})")
        print(f"   HODNOCENI: {h.get('rating', 0)} / 5")
        print(f"   PLATFORMY: {', '.join(h.get('platformy', []))}")
        print(f"   ZANRY: {', '.join(h.get('zanry', []))}")
        print("-" * 30)


def menu():
    while True:
        print("\n   --- HERNI FILTR ---")
        print("1. Hledat podle zanru")
        print("2. Hledat podle platformy")
        print("3. Pokrocily filtr (strict)")
        print("4. TOP 10 her podle roku")
        print("5. Stastny los (nahodna hra)")
        print("6. Konec")

        volba = input("Zadejte volbu: ")

        if volba == "1":
            z = input("Zadej zanry (napr. action,rpg): ")
            tiskni(vyhledej_hry(genres=z))

        elif volba == "2":
            p = input("Zadej platformy (napr. pc,ps5): ")
            tiskni(vyhledej_hry(platforms=p))

        elif volba == "3":
            z = input("Zadej povinne zanry: ")
            p = input("Zadej platformy: ")
            tiskni(vyhledej_hry(genres=z, platforms=p, strict=True))

        elif volba == "4":
            rok = input("Zadej rok: ")
            if rok.isdigit():
                tiskni(get_top_10_by_year(rok))

        elif volba == "5":
            z = input("Zanr (nepovinne): ")
            p = input("Platforma (nepovinne): ")
            print("Losuji...")
            hra = get_random_game(genres=z, platform=p)
            # Tady voláme tiskni s parametrem specialni_text
            tiskni(hra, specialni_text="--- STASTNA HRA NALEZENA ---")

        elif volba == "6":
            print("Zabavne hrani...")
            break