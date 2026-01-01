import streamlit as st
import pandas as pd
from api_manager import vyhledej_hry, get_top_10_by_year, get_random_game

# Konfigurace stranky
st.set_page_config(page_title="Herni Katalog PRO", page_icon="🎮", layout="wide")

# CSS Design
st.markdown("""
    <style>
    .stDataFrame { background-color: #1e2130; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #ff4b4b; color: white; font-weight: bold; height: 3em; }
    .luck-box { background-color: #1e2130; padding: 30px; border-radius: 15px; border: 2px solid #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

MOJE_PLATFORMY = ["pc", "ps5", "ps4", "ps3", "ps2", "xbox-series", "xbox-one", "switch"]

with st.sidebar:
    st.title("🕹️ Vyhledávač")
    volba = st.sidebar.radio("Menu:", ["Hledat podle zanru", "Hledat podle platformy", "Kombinovane hledani",
                                       "TOP 10 podle roku", "Šťastný los"])


def priprav_df(data):
    df = pd.DataFrame(data)
    if not df.empty:
        df['zanry'] = df['zanry'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        df['platformy'] = df['platformy'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    return df


# --- SEKCE ---

if volba == "Hledat podle zanru":
    st.header("🔍 Hledání podle žánru")
    z = st.text_input("Zadejte žánry (např. action, rpg):")
    if st.button("Spustit hledání podle žánru"):
        if z:
            vysledky = vyhledej_hry(genres=z)
            if vysledky:
                st.dataframe(priprav_df(vysledky), use_container_width=True, hide_index=True)
            else:
                st.warning("Podle tohoto žánru jsem nic nenašel.")
        else:
            st.info("Nejdříve napiš nějaký žánr.")

elif volba == "Hledat podle platformy":
    st.header("📱 Hledání podle platformy")
    p = st.selectbox("Vyberte zařízení:", MOJE_PLATFORMY)
    if st.button("Zobrazit hry pro tuto platformu"):
        st.dataframe(priprav_df(vyhledej_hry(platforms=p)), use_container_width=True, hide_index=True)

elif volba == "Kombinovane hledani":
    st.header("👾 Kombinované hledání")
    c1, c2 = st.columns(2)
    with c1:
        z_in = st.text_input("Žánry:")
    with c2:
        p_in = st.multiselect("Platformy:", MOJE_PLATFORMY)

    if st.button("📊 Generovat tabulku výsledků"):
        if z_in or p_in:
            p_string = ",".join(p_in)
            vysledky = vyhledej_hry(genres=z_in, platforms=p_string, strict=True)
            if vysledky:
                st.dataframe(priprav_df(vysledky), use_container_width=True, hide_index=True)
            else:
                st.warning("Nic nenalezeno pro tuto kombinaci.")
        else:
            st.info("Zadej aspoň žánr nebo vyber platformu.")

elif volba == "TOP 10 podle roku":
    st.header("🏆 Žebříček roku")
    rok = st.slider("Zvolte rok:", 1995, 2025, 2022)
    if st.button("Ukázat TOP 10 nejlepších her"):
        vysledky = get_top_10_by_year(str(rok))
        if vysledky:
            for i, h in enumerate(vysledky, 1):
                st.markdown(
                    f"<div style='background-color: #1e2130; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4b4b;'><h3>{i}. {h['jmeno']}</h3><p>⭐ {h['rating']} | {', '.join(h['platformy'])}</p></div>",
                    unsafe_allow_html=True)
        else:
            st.error("Pro tento rok nemám žádná data.")

elif volba == "Šťastný los":
    st.header("🎲 Vylosuj si svoji hru")
    c1, c2, c3 = st.columns(3)
    with c1:
        p_l = st.selectbox("Platforma:", MOJE_PLATFORMY)
    with c2:
        z_l = st.text_input("Žánr (volitelné):")
    with c3:
        r_l = st.text_input("Rok (volitelné):")

    if st.button("🎰 Vylosovat náhodnou hru"):
        h = get_random_game(genres=z_l, platform=p_l, year=r_l)
        if h:
            st.balloons()
            # ODSTRANĚNO HODNOCENÍ Z VÝPISU
            st.markdown(f"""
                <div class='luck-box'>
                    <h1 style='color: #ff4b4b;'>{h['jmeno']}</h1>
                    <h3>📅 Rok vydání: {h['rok']}</h3>
                    <p style='font-size: 1.1em;'><b>Žánry:</b> {', '.join(h['zanry'])}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Pro toto zadání se nepodařilo nic vylosovat.")



