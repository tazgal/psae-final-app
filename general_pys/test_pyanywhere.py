
import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser


def rn_show_greek_economy_news_buttons():
    st.subheader("Οικονομικές Ειδήσεις")
    
    news_sites = {
        "OT.gr": "https://www.ot.gr",
        "Ναυτεμπορική": "https://www.naftemporiki.gr/finance/economy/",
        "Καθημερινή": "https://www.kathimerini.gr/economy/",
        "Capital": "https://www.capital.gr/oikonomia"
    }

    for name, url in news_sites.items():
        if st.button(name):
            webbrowser.open(url)

    st.divider()

    if st.button("📂 Άνοιγμα οικονομικών"):
        for url in news_sites.values():
            webbrowser.open(url)


open_menu = option_menu(
        "Άνοιξε σελίδες",
        ["Παραπολιτικά", "Βουλή", "Γενικά", "Oικονομικές σελίδες", "Διεθνής Οικονομία", "Διεθνή", "Ραδιόφωνα"]
    )

    
if open_menu == "Oικονομικές σελίδες":
        rn_show_greek_economy_news_buttons()
