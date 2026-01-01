
from api_manager import vyhledej_hry, get_top_10_by_year


def tiskni(vysledky):
    if not vysledky:
        print("\n--- Zadna hra neodpovida zadani ---")
        return

    print(f"\nNalezeno {len(vysledky)} her:")
    for h in vysledky:
        print(f"-> {h['jmeno'].upper()} ({h['rok']})")
        print(f"   HODNOCENI: {h['rating']} / 5")
        print(f"   PLATFORMY: {', '.join(h['platformy'])}")
        print(f"   ZANRY: {', '.join(h['zanry'])}")
        print("-" * 30)


def menu():
    while True:
        print("\n   --- HERNI FILTR ---")
        print("1. Hledat podle zanru (aspon jeden)")
        print("2. Hledat podle platformy (aspon jedna)")
        print("3. Pokrocily filtr (zanry + jedna z platforem)")
        print("4. TOP 10 her podle roku")
        print("5. Konec")

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
            tiskni(vyhledej_hry(genres=z, platforms=p, strict_genres=True))

        elif volba == "4":
            rok = input("Zadej rok (napr. 2023): ")
            if rok.isdigit():
                tiskni(get_top_10_by_year(rok))
            else:
                print("Chyba: Zadej platny rok (cislo).")

        elif volba == "5":
            print("Koncim...")

            break
