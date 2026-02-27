import streamlit as st
from streamlit_option_menu import option_menu
from mod_01_enter_open import add_text_agenda_streamlit, add_text_shmeioseis_streamlit,create_or_append_txt_streamlit
from mod_02_rss_feeds import feed_read_902_streamlit, feed_read_rizospastis_streamlit
from mod_02_read_news import (read_news_titles_fix, 
                              read_news_titles_with_links,
                              read_news_links_for_st,
                              vimatodotis_for_streamlit, 
                              big_mouth_for_streamlit,
                              apocryptografos_for_streamlit,
                              read_parapolitika_all_streamlit,
                              big_mouth_for_streamlit2,
                              read_titles_streamlit,
                              read_titles_geopol_streamlit,
                              read_titles_pol_streamlit,
                              read_titles_economy_streamlit,
                              rn_open_greek_economy_news,
                              rn_global_economy_news,
                              rn_vouli,
                              rn_radios
)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import webbrowser 
from mod_06_NLP import nlp_spacy_ner_grouped_entities,extract_date_sentences
from mod_07_transformers import tr_generate_title_streamlit,tr_generate_summary_streamlit
from mod_11_translation import translate_el_streamlit, translate_el_streamlit2
from mod_05_sql import sq_search_to_titles_streamlit2
from mod_05_other_dbs import (agenda_streamlit,show_last_agenda_stream,search_agenda_date_streamlit)
from mod_08_geo import (scr_from_text_to_map_streamlit)
from mod_12_journal import imerologio
from mod_13_transcript import transcribe_youtube_streamlit,transcribe_mp3_streamlit,transcribe_mp3_streamlit2
from mod_14_ocr import ocr_reader_streamlit
from mod_15_GPTs import gpt_deepseek_streamlit_short2, gpt_deepseek_vasika_simeia
from mod_18_scripts import scr_from_news_to_db_and_persons3_streamlit


# ********************* DEFS *********************



# ********************* TEST AREA *********************

st.markdown("# News toolbox (test2)")

st.sidebar.title("Κύριο μενού")
main_menu = st.sidebar.radio(
    "Κύριο μενού", 
    ["Ριζοσπάστης - 902", "Πρωτοσέλιδα", "Ειδήσεις", "Αποδελτίωση", 
     "Scrap Τίτλοι", "Tools", "Σημειωματάριο", "Ημερολόγιο"]
)


####
if main_menu == "Ριζοσπάστης - 902":
    rizospastis_menu = option_menu(
        "Ριζοσπάστης menu",
        ["Άνοιξε τον Ριζοσπάστη","Ριζοσπάστης_RSS","Ανοιξε τον 902","902_feed"]

    )
    st.write("Welcome to news toolbox")
    if rizospastis_menu == "Άνοιξε τον Ριζοσπάστη":
        webbrowser.open_new_tab("https://www.rizospastis.gr")
    elif rizospastis_menu == "Ριζοσπάστης_RSS":
        feed_read_rizospastis_streamlit()
    elif rizospastis_menu == "Ανοιξε τον 902":
        webbrowser.open_new_tab("https://www.902.gr")
    elif rizospastis_menu == "902_feed":
        feed_read_902_streamlit()


elif main_menu == "Πρωτοσέλιδα":
        webbrowser.open_new_tab("https://www.frontpages.gr")

elif main_menu == "Scrap Τίτλοι":
    titles_menu = option_menu(
        "Scrap τίτλοι",
        ["Τίτλοι γεωπολιτικά", "Τίτλοι πολιτική", "Τίτλοι οικονομία","Ψάξε σε τίτλους","Κάνε scrap τίτλους"]
    )

    if titles_menu == "Τίτλοι γεωπολιτικά":
        read_titles_geopol_streamlit()
    elif titles_menu == "Τίτλοι πολιτική":
        read_titles_pol_streamlit()
    elif titles_menu == "Τίτλοι οικονομία":
        read_titles_economy_streamlit()
    elif titles_menu == "Ψάξε σε τίτλους":
        sq_search_to_titles_streamlit2()
    elif titles_menu == "Κάνε scrap τίτλους":
        scr_from_news_to_db_and_persons3_streamlit()


elif main_menu == "Ειδήσεις":
    open_menu = option_menu(
        "Άνοιξε σελίδες",
        ["Παραπολιτικά", "Σήμερα στη Βουλή", "Oικονομικές σελίδες", "Διεθνής Οικονομία","Ραδιόφωνα"]
    )

    
    if open_menu == "Oικονομικές σελίδες":
        rn_open_greek_economy_news()
    elif open_menu == "Διεθνής Οικονομία":
        rn_global_economy_news()
    elif open_menu == "Παραπολιτικά":
        read_parapolitika_all_streamlit()
    elif open_menu == "Σήμερα στη Βουλή":
        rn_vouli()
    elif open_menu == "Ραδιόφωνα":
        rn_radios()

elif main_menu == "Tools":
    user_text = st.text_area("Βάλε το ελληνικό κείμενο εδώ:", height=200)

    if st.button("Πρότεινε τίτλο"):
        tr_generate_title_streamlit(user_text)
    
    if st.button("Περίληψη"):
        tr_generate_summary_streamlit(user_text)

    if st.button("Βασικά σημεία"):
        gpt_deepseek_vasika_simeia(user_text)

    # Κουμπί για να τρέξει η επεξεργασία
    if st.button("Πρόσωπα και Οργανισμοί"):
        if user_text.strip():
            results = nlp_spacy_ner_grouped_entities(user_text)
            # Εμφάνιση αποτελεσμάτων με μορφοποίηση
            st.subheader("Αποτελέσματα:")
            for label, ents in results.items():
                st.write(f"**{label}**: {', '.join(ents)}")
        else:
            st.warning("Γράψε πρώτα κείμενο!")
    
    if st.button("Βρες ημερομηνίες"):
        extract_date_sentences(user_text)

    if st.button("Χάρτης"):
        scr_from_text_to_map_streamlit(user_text)


    if st.button("Μετάφραση από αγγλικά"):
        translate_el_streamlit2(user_text)
    
    if st.button("Απομαγνητοφώνηση από youtube"):
        transcribe_youtube_streamlit()
    
    uploaded = st.file_uploader(
            "Επέλεξε ένα αρχείο MP3 για απομαγνητοφώνηση",
            type=["mp3"]
        )
    if st.button("Aπομαγνητοφώνηση από mp3"):
        transcribe_mp3_streamlit2(uploaded)

    uploaded_photo = st.file_uploader(
    "Επέλεξε ένα αρχείο εικόνας για OCR",
    type=["jpg", "png"]  # αν θες μόνο εικόνες
    )
    if uploaded_photo and st.button("OCR από εικόνα"):
        ocr_reader_streamlit(uploaded_photo)


    
elif main_menu == "Αποδελτίωση":
    
    if st.button("Σημερινή ατζέντα"):
        show_last_agenda_stream()

    date = st.text_input("Δώσε ημερομηνία (π.χ. 24/09)")
    if st.button("Ψάξε ατζέντα με ημερομηνία"):
        if date.strip():
            search_agenda_date_streamlit(date.strip())
        else:
            st.warning("Γράψε πρώτα ημερομηνία.")
    
    if st.button("Δες τα όλα"):
        agenda_streamlit()

elif main_menu == "Σημειωματάριο":
        text_for_agenda = st.text_area("Βάλε το ελληνικό κείμενο εδώ:", height=200)
        if st.button("Πρόσθεσε το κείμενο στην ατζέντα"):
            add_text_agenda_streamlit(text_for_agenda)
        if st.button("Πρόσθεσε το κείμενο στις σημειώσεις"):
            add_text_shmeioseis_streamlit(text_for_agenda)
        
        file_name = st.text_input("Δώστε όνομα στο αρχείο (χωρίς κατάληξη)")
        if st.button("Σώσε σε ένα νέο κείμενο"):
            create_or_append_txt_streamlit(file_name,text_for_agenda)

elif main_menu == "Ημερολόγιο":
        imerologio()


