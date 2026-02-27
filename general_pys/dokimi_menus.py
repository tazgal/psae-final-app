import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    main_menu = option_menu(
        "Κύριο Μενού",
        ["Ριζοσπάστης - 902", "Πρωτοσέλιδα", "Ειδήσεις", "Αποδελτίωση", "ΒΔ Ειδήσεων","Scrap Τίτλοι", "Tools","Economy Tools", "NLP", "Απομαγνητοφώνηση κτλ", "GPTs", "Σημειωματάριο", "Ημερολόγιο"],
        icons=["house", "newspaper", "globe", "calendar-event","database","database","tools","tools", "tools","mic","globe","journal-text","calendar"],
        menu_icon="cast",
        default_index=0
    )

if main_menu == "Ριζοσπάστης - 902":
    rizospastis_menu = option_menu(
        "Ριζοσπάστης menu",
        ["Άνοιξε τον Ριζοσπάστη","Ριζοσπάστης_RSS","Ανοιξε τον 902","902_feed"]

    )

    if rizospastis_menu == "Ριζοσπάστης_RSS":
           with st.expander("Διάλεξε για Ριζοσπάστη"):
            st.button("Click me baby")
            st.button("ΒΔ Ριζοσπάστη")
        