

######## 
########  Περίοδος ενασχόλησης 30/12/2025 - 16/1/2026

# ============================================================
# Τι έγινε
# ============================================================

######### Φίλτρα σε ΒΔ
# Διαχείριση ΒΔ
#    Δημιουργία νέας, 
# #    Μενού που να ενσωματωθεί το παλιό 
# Συμμάζεμα NewsRoom Tools 
#  # from one to another
# Να διαβάζει τελευταία ατζέντα
# Ενα πεδίο για γράψιμο που 1. να μπορεί να αλλάζει, bold κτλ. Να έχει δεξιά ένα άλλο column; 
    # όπου να μπορεί να έχει ανοιχτά άλλα αρχεία, πχ σημειώσεις, εικόνες, df, 
# Να ανοίγει περιεχόμενα φακέλου 
# Economy section 
    # Περιοχή εργασίας οικονομία
    # Ανοιγμα pdf (και σημειώσεις στο πλάι κτλ)
# Εμφάνιση και δημιουργεία Charts
# yaml πρώτη απόπειρα και json κοκ 


# ============================================================
# To DO NEXT
# ============================================================

# Πηγές - Να ανοίγει όλες τις σχετικές ιστοσελίδες (σε όλες τις σελίδες)
# Ημερολόγιο με κατηγορίες και δυνατότητα διαγραφής 
# Διάβασμα ατζέντας ανά μήνα (με st.selectbox)

# scrap ειδήσεων με συγκεκριμένη ώρα 

# ΓΙΑ ΠΕΡΙΕΧΟΜΕΝΟ 
# Φτιάξιμο Βάσεων Δεδομένων για εταιρείες
#  Λεξικά Οικονομικών όρων 


#
#
#

# ============================================================
# ΠΕΡΙΕΧΟΜΕΝΑ
# ============================================================

# 732 - Agenda 
# 845 - Journal 
# 1100 - Database
# 1481 - Economy Tools
# 



# ============================================================
# ΒΑΣΙΚΕΣ ΒΙΒΛΙΟΘΗΚΕΣ
# ============================================================

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_navigation_bar import st_navbar 
import requests
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser
from docx import Document
from pathlib import Path
import sqlite3
from datetime import date, timedelta
import streamlit.components.v1 as components
from natural_pdf import PDF
import fitz
from streamlit_pdf_viewer import pdf_viewer
import tempfile
import io 
from PIL import Image
from datetime import datetime




# ============================================================
# 📁 MODULE 01 — Εισαγωγή, Άνοιγμα Αρχείων, PDF, Pandas
# ============================================================
from mod_01_enter_open import *

from mod_01_pdf import *
from mod_01_pandas_charts import *
from mod_01_one_to_another import *

from mod_01_yaml import * 

# ============================================================
# 📁 MODULE 02 — RSS Feeds & News Reading
# ============================================================
from mod_02_rss_feeds import (
    feed_read_902_streamlit,
    feed_read_rizospastis_streamlit,
    feed_google_news_streamlit,
    feed_to_R_db,
    show_R_DB_streamlit,
    show_R_DB_streamlit2
)

from mod_02_read_news import (
    apocryptografos_for_streamlit,
    big_mouth_for_streamlit,
    big_mouth_for_streamlit2,
    read_news_links_for_st,
    read_news_titles_fix,
    read_news_titles_with_links,
    read_parapolitika_all_streamlit,
    read_titles_economy_streamlit,
    read_titles_geopol_streamlit,
    read_titles_pol_streamlit,
    read_titles_streamlit,
    rizos_apopsi,
    rn_global_economy_news,
    rn_global_economy_news_buttons,
    rn_global_economy_news_tabs,
    rn_open_greek_economy_news,
    rn_radios,
    rn_economy_news_buttons,
    rn_show_brics_news,
    rn_show_diethni_news,
    rn_show_geopolitics_news,
    rn_show_general_news,
    rn_show_greek_economy_news_buttons,
    rn_vouli,
    vimatodotis_for_streamlit,
    rn_dieftinseis,
    rn_sources_selector,
    render_sources_selector,
    rn_load_sources
)

from mod_02_scrap import scrape_evdomadiaio_deltio_html, scrap_praktika, scrap_praktika_structured

# ============================================================
# 📁 MODULE 05 — SQL Databases
# ============================================================
from mod_05_sql import sq_search_to_titles_streamlit2
from mod_05_sql_streamlit import main_db_streamlit
from mod_05_other_dbs import (
    agenda_streamlit,
    search_agenda_date_streamlit,
    search_agenda_date_streamlit2,
    show_last_agenda_stream,
    show_last_agenda_stream2,
    load_txt_agenda_folder,
)
from mod_05_sql_telikes import *


# ============================================================
# 📁 MODULE 06 — NLP & Λεξικά
# ============================================================
from mod_06_NLP import (
    extract_date_sentences,
    nlp_spacy_ner_grouped_entities
)

from mod_06_lexicon import (
    lex_add_links_exoteriko,
    lex_oikonomikon,
    lex_semantics_geo
)

from mod_06_lexicon1 import lexiko_custom_show


# ============================================================
# 📁 MODULE 07 — Transformers (Title & Summary Generation)
# ============================================================
from mod_07_transformers import (
    tr_generate_title_streamlit,
    tr_generate_summary_streamlit
)


# ============================================================
# 📁 MODULE 08 — GEO Mapping
# ============================================================
from mod_08_geo import scr_from_text_to_map_streamlit


# ============================================================
# 📁 MODULE 11 — Translation (EN↔EL)
# ============================================================
from mod_11_translation import (
    translate_el_streamlit,
    translate_el_streamlit2
)


# ============================================================
# 📁 MODULE 12 — Journal / Diary
# ============================================================
from mod_12_journal import imerologio


# ============================================================
# 📁 MODULE 13 — Transcription Tools
# ============================================================
from mod_13_transcript import (
    transcribe_youtube_streamlit,
    transcribe_mp3_streamlit,
    transcribe_mp3_streamlit2
)


# ============================================================
# 📁 MODULE 14 — OCR
# ============================================================
from mod_14_ocr import ocr_reader_streamlit


# ============================================================
# 📁 MODULE 15 — GPT tools
# ============================================================
from mod_15_GPTs import (
    gpt_deepseek_streamlit_short2,
    gpt_deepseek_vasika_simeia,
    gpt_deepseek_diorthosi,
    gpt_mistral_alli_diatiposi_streamlit,
    gpt_mistral_anakoinosi_streamlit,
    gpt_mistral_diorthosi_streamlit,
    gpt_mistral_general_streamlit,
    gpt_mistral_oikonomia_streamlit,
    gpt_mistral_plagios_streamlit
)


# ============================================================
# 📁 MODULE 16 — Images / Search Images
# ============================================================
from mod_16_images2 import search_images2


# ============================================================
# 📁 MODULE 18 — Scripts / Scraping to DB & Persons
# ============================================================
from mod_18_scripts import scr_from_news_to_db_and_persons3_streamlit


# ============================================================
# 📁 MODULE 22 — PDF to RAG
# ============================================================
from mod_22_pdf_to_rag import pdf_to_rag_streamlit


# ============================================================
# 📁 MODULE 22 — Writing Area 
# ============================================================
from mod_23_my_writing_area import main_writing_area


# ********************* DATA etc *********************

DATABASES = {
    "📰 News DB": {
        "path": "DBs/news_05.db",
        "read_only": False
    },
    "👤 Agenda DB": {
        "path": "DBs/agenda.db",
        "read_only": False
    },
    "Rizos DB": {
        "path": "DBs/news_rss_R3.db",
        "read_only": False
    },
    "👤 Tasks": {
        "path": "DBs/tasks.db",
        "read_only": False
    },
    "Companies": {
        "path": "DBs/companies.db",
        "read_only": False
    }

}

# ********************* TEST AREA *********************

st.set_page_config(page_title="",layout="wide")

with st.sidebar:
    main_menu = option_menu(
        "Main menu",
        [ 
        "Sources", 
        "Agenda",
        "Databases", 
        "NewsRoom Tools",
        "Economy Tools",
        "NLP", "RAG", "GPTs"],
        icons=["newspaper","calendar-event", "database", "house", "globe", "database","tools","tools", "tools","mic","bar-chart", "robot", "globe","journal-text","calendar"],
        menu_icon="cast",
        default_index=0,
        )


if main_menu == "Sources":
    
    df_piges = rn_load_sources()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10  = st.tabs([
                                "Πρωτοσέλιδα",
                                "Ριζοσπάστης - 902",
                                "News",
                                "Economy",
                                "Global economy",
                                "International",
                                "Parapolitics",
                                "Parliament - Government",
                                "Podcasts - Radios",
                                "Notes"
                                ])
    
    
    with tab1:
        st.subheader("Frontpages")

        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

        

        with col1:
            st.components.v1.iframe(
                "https://www.frontpages.gr",
                height=800,
                scrolling=True
            )
        
        
        with col2:
            st.link_button("Ανοιξε ιστοσελίδα με πρωτοσέλιδα","https://www.frontpages.gr")
            
            st.markdown("---")
            notes1 = st.text_area("📝 Notes",key="notes1",height=300)
            if st.button("Save note",key="b1"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes1)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")


    with tab2:
        st.subheader("Rizospastis")
        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

        with col2:
        
            choiceR = st.selectbox("Rizos_choose",["Rizos Main","Main articles","Opinion","Save to db","Rizos_DB","902_rss"], index=0)

            st.link_button("Ανοιξε τον Ριζοσπάστη", "https://www.rizospastis.gr")
            st.link_button("Ανοιξε τον 902","https://www.902.gr")

            st.markdown("---")
            notes2 = st.text_area("📝 Notes",key="notes2",height=300)
            if st.button("Save note",key="b2"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes2)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")

        
        with col1:

            if choiceR == "Rizos Main":
                st.components.v1.iframe(
                    "https://www.rizospastis.gr",
                    height=800,
                    scrolling=True
                )

            elif choiceR == "Main articles":
                feed_read_rizospastis_streamlit()
            elif choiceR == "Opinion":
                rizos_apopsi()
            elif choiceR == "Save to db":
                feed_to_R_db()
            elif choiceR == "Rizos_DB":
                show_R_DB_streamlit()
            elif choiceR == "902_rss":
                feed_read_902_streamlit()


    with tab3:
        st.subheader("News")
        general_cols1, general_cols2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

           
        with general_cols2:
            df_cat = df_piges[df_piges["category"] == "news"]

            subcategories = sorted(
                df_cat["subcategory"].dropna().unique()
             )

            selected_sub = st.selectbox(
                "Choose group",
                ["All"] + subcategories
            )

            if selected_sub != "All":
                df_cat = df_cat[df_cat["subcategory"] == selected_sub]

            if df_cat.empty:
                st.info("Δεν υπάρχουν πηγές.")
            else:
                source = st.selectbox(
                    "Economy Sources",
                    df_cat["name"].tolist()
                )

                url = df_cat.loc[df_cat["name"] == source, "url"].values[0]
                st.session_state["iframe_url"] = url

                st.link_button("Άνοιγμα σε νέο tab", url)

            st.markdown("---")
            if st.button("Open all in new tabs",help="Check pop up windows if it does not open"):
                js = ""
                for url in df_cat["url"]:
                    js += f'window.open("{url}", "_blank");'
                components.html(f"<script>{js}</script>", height=0)


            st.markdown("---")
            notes3 = st.text_area("📝 Notes",key="notes3",height=300)
            if st.button("Save note",key="b3"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes3)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")


        with general_cols1:
                if "iframe_url" in st.session_state:
                    st.components.v1.iframe(
                        st.session_state["iframe_url"],
                        height=800,
                        scrolling=True
                    )
                    st.caption(
                        "⚠️ Αν η σελίδα δεν εμφανίζεται, παρακαλώ ανοίξτε την ιστοσελίδα σε νέο tab."
                        )
                else:
                    st.info("Επίλεξε μια πηγή για προβολή.")
            
               
    with tab4:
        st.subheader("Economy")
        ec_cols1, ec_cols2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")
        
        with ec_cols2:
            df_cat = df_piges[df_piges["category"] == "economy"]

            subcategories = sorted(
                df_cat["subcategory"].dropna().unique()
            )

            selected_sub = st.selectbox(
                "Choose group",
                ["Όλες"] + subcategories
            )

            if selected_sub != "Όλες":
                df_cat = df_cat[df_cat["subcategory"] == selected_sub]

            if df_cat.empty:
                st.info("Δεν υπάρχουν πηγές.")
            else:
                source = st.selectbox(
                    "Economy Sources",
                    df_cat["name"].tolist()
                )

                url = df_cat.loc[df_cat["name"] == source, "url"].values[0]
                st.session_state["iframe_url"] = url

                st.link_button("Άνοιγμα σε νέο tab", url)

            
            st.markdown("---")
            notes4 = st.text_area("📝 Notes",key="notes4",height=300)
            if st.button("Save note",key="b4"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes4)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")


        with ec_cols1:
            if "iframe_url" in st.session_state:
                st.components.v1.iframe(
                    st.session_state["iframe_url"],
                    height=800,
                    scrolling=True
                )
                st.caption(
                    "⚠️ Αν η σελίδα δεν εμφανίζεται, παρακαλώ ανοίξτε την ιστοσελίδα σε νέο tab."
                    )
            else:
                st.info("Επίλεξε μια πηγή για προβολή.")
            

            


    with tab5:
        st.subheader("Global Economy")
        global_col1, global_col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

        

        with global_col2:
            df_cat = df_piges[df_piges["category"] == "global economy"]

            subcategories = sorted(
                df_cat["subcategory"].dropna().unique()
            )

            selected_sub = st.selectbox(
                "Choose group",
                ["Όλες"] + subcategories
            )

            if selected_sub != "Όλες":
                df_cat = df_cat[df_cat["subcategory"] == selected_sub]

            if df_cat.empty:
                st.info("Δεν υπάρχουν πηγές.")
            else:
                source = st.selectbox(
                    "Global economy Sources",
                    df_cat["name"].tolist()
                )

                url = df_cat.loc[df_cat["name"] == source, "url"].values[0]
                st.session_state["iframe_url"] = url

                st.link_button("Άνοιγμα σε νέο tab", url)
            

            st.markdown("---")
            if st.button("open google news",key="gnews",help="press to open google news"):
                feed_google_news_streamlit()
            

            st.markdown("---")
            notes5 = st.text_area("📝 Notes",key="notes5",height=300)
            if st.button("Save note",key="b5"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes5)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")

            

        with global_col1:
            
            if st.button("open google news",key="gnews_main",help="press to open google news"):
                feed_google_news_streamlit()

            if "iframe_url" in st.session_state:
                st.components.v1.iframe(
                    st.session_state["iframe_url"],
                    height=800,
                    scrolling=True
                )
                st.caption(
                    "⚠️ Αν η σελίδα δεν εμφανίζεται, παρακαλώ ανοίξτε την ιστοσελίδα σε νέο tab."
                    )
            
            else:
                st.info("Επίλεξε μια πηγή για προβολή.")


    with tab6:
        st.subheader("International")
        int_cols1, int_cols2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

        with int_cols2:
            df_cat = df_piges[df_piges["category"] == "international sources"]

            subcategories = sorted(
                df_cat["subcategory"].dropna().unique()
            )

            selected_sub = st.selectbox(
                "Choose group",
                ["Όλες"] + subcategories
            )

            if selected_sub != "Όλες":
                df_cat = df_cat[df_cat["subcategory"] == selected_sub]

            if df_cat.empty:
                st.info("Δεν υπάρχουν πηγές.")
            else:
                source = st.selectbox(
                    "International Sources",
                    df_cat["name"].tolist()
                )

                url = df_cat.loc[df_cat["name"] == source, "url"].values[0]
                st.session_state["iframe_url"] = url

                st.link_button("Άνοιγμα σε νέο tab", url)


            st.markdown("---")
            notes6 = st.text_area("📝 Notes",key="notes6",height=300)
            if st.button("Save note",key="b6"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes6)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")

        with int_cols1:
            if "iframe_url" in st.session_state:
                st.caption(
                    "⚠️ Αν η σελίδα δεν εμφανίζεται, παρακαλώ ανοίξτε την ιστοσελίδα σε νέο tab."
                    )
                
                st.components.v1.iframe(
                    st.session_state["iframe_url"],
                    height=600,
                    scrolling=True
                )
                
            
            else:
                st.info("Επίλεξε μια πηγή για προβολή.")




    with tab7:
        st.subheader("Παραπολιτικά")
        par_cols1, par_cols2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

        with par_cols2:

            df_cat = df_piges[df_piges["category"] == "parapolitical"]

            subcategories = sorted(
                df_cat["subcategory"].dropna().unique()
             )

            selected_sub = st.selectbox(
                "Choose group",
                ["All"] + subcategories
            )

            if selected_sub != "All":
                df_cat = df_cat[df_cat["subcategory"] == selected_sub]


            if df_cat.empty:
                st.info("Δεν υπάρχουν πηγές.")
            else:
                source = st.selectbox(
                    "Economy Sources",
                    df_cat["name"].tolist()
                )

                url = df_cat.loc[df_cat["name"] == source, "url"].values[0]
                st.session_state["iframe_url_parapolitika"] = url

                st.link_button("Άνοιγμα σε νέο tab", url)

                st.markdown("---")

                notes7 = st.text_area("📝 Notes",key="notes7",height=300)
                if st.button("Save note",key="b7"):
                    file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(notes7)
                    st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")
        
        with par_cols1:

            if st.button("open rss main parapolitics"):
               read_parapolitika_all_streamlit()
            elif "iframe_url_parapolitika" in st.session_state:
                st.components.v1.iframe(
                    st.session_state["iframe_url_parapolitika"],
                    height=800,
                    scrolling=True
                )
                st.caption(
                    "⚠️ Αν η σελίδα δεν εμφανίζεται, παρακαλώ ανοίξτε την ιστοσελίδα σε νέο tab."
                    )
            
            else:
                st.info("Επίλεξε μια πηγή για προβολή.")

            


    with tab8:
        st.subheader("Parliament - Government")
        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")


        with col2:
            choice_bouli = st.selectbox("Διάλεξε από σελίδα βουλής",["Πρόγραμμα Βουλής","Πρακτικά","Vouliwatch","Government","Prime minister"])

            if st.button("Άνοιγμα σε νέο tab"):
                if choice_bouli == "Πρόγραμμα Βουλής":
                    webbrowser.open_new_tab(
                        "https://www.hellenicparliament.gr/Nomothetiko-Ergo/dailyplan"
                    )
                    webbrowser.open_new_tab(
                        "https://www.hellenicparliament.gr/Koinovouleftikes-Epitropes/Evdomadiaio-Deltio"
                    )

                elif choice_bouli == "Vouliwatch":
                    webbrowser.open_new_tab("https://vouliwatch.gr/news")

                elif choice_bouli == "Πρακτικά":
                    webbrowser.open_new_tab(
                        "https://www.hellenicparliament.gr/Praktika/Synedriaseis-Olomeleias"
                    )
                elif choice_bouli == "Prime minister":
                    webbrowser.open_new_tab("https://www.primeminister.gr")
                
                elif choice_bouli == "Government":
                    webbrowser.open_new_tab("https://media.gov.gr")
            
            st.markdown("---")
            notes8 = st.text_area("📝 Notes",key="notes8",height=300)
            if st.button("Save note",key="b8"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(notes8)
                st.success("Το κείμενο αποθηκεύτηκε στις Σημειώσεις!")



        with col1:
            
            if choice_bouli == "Πρόγραμμα Βουλής":
                html = scrape_evdomadiaio_deltio_html()
                st.components.v1.html(html, height=700, scrolling=True)
            elif choice_bouli == "Vouliwatch":
                st.components.v1.iframe(
                    "https://vouliwatch.gr/news",
                    height=800,
                    scrolling=True
                )
            elif choice_bouli == "Πρακτικά":
                html2 = scrap_praktika()
                if html2:
                    st.components.v1.html(
                        f"""
                        <html>
                        <head>
                            <meta charset="utf-8">
                        </head>
                        <body>
                            <table border="1" width="100%">
                                {html2}
                            </table>
                        </body>
                        </html>
                        """,
                        height=700,
                        scrolling=True
                    )
                else:
                    st.warning("Δεν βρέθηκαν πρακτικά.")

    with tab9:
        st.subheader("Podcasts - Radio")
        radio_cols1, radio_cols2 = st.columns(
            ([4,1]), 
            gap="small", 
            vertical_alignment="top", 
            border=True)

        with radio_cols2:
            if "radios" not in st.session_state:
                st.session_state.radios = True


            st.text("902 podcast libary")
            if st.button("See my podcasts"):
                st.session_state.radios = True

                

                

        with radio_cols1:
            if st.session_state.radios:
                
                playlists = {
                    "01_Ακρίβεια": "https://www.youtube.com/watch?v=UrUg0668Xr8&list=PLQZVPd1pcxwkOfRfzea7iRaNzxygYon7x&index=2",
                    "02_Προϋπολογισμός": "https://www.youtube.com/watch?v=YpwpuOWN38E&list=PLQZVPd1pcxwkOfRfzea7iRaNzxygYon7x&index=1"
                }

                selected = st.selectbox("Επιλογή playlist", playlists.keys())

                episode_id = playlists[selected]

                st.video(f"{episode_id}")




    with tab10: 
        st.subheader("Notes")

        

        if "check_sources" not in st.session_state:
            st.session_state["check_sources"] = False

        if "show_agenda" not in st.session_state:
            st.session_state["show_agenda"] = False

        if "show_add_agenda" not in st.session_state:
            st.session_state["show_add_agenda"] = False


        notes_col1, notes_col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")
        
        with notes_col2:

            if st.button("Check notes"):
                st.session_state["check_sources"] = False
                st.session_state["show_agenda"] = False
                st.session_state["show_add_agenda"] = False

            if st.button("Check sources"):
                st.session_state["check_sources"] = True
                st.session_state["show_agenda"] = False
                st.session_state["show_add_agenda"] = False

            st.markdown("---")

            if st.button("Show my agenda"):
                st.session_state["show_agenda"] = True
                st.session_state["check_sources"] = False
                st.session_state["show_add_agenda"] = False

            if st.button("Change my agenda df"):
                st.session_state["show_agenda"] = True
                st.session_state["check_sources"] = False
                st.session_state["show_add_agenda"] = False

            st.markdown("---")

            if st.button("Add to my agenda"):
                st.session_state["show_add_agenda"] = not st.session_state["show_add_agenda"]

            st.markdown("---")

            if st.button("Clear notes"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("----- New notes -----")

            
    
        
        with notes_col1:

            if not st.session_state["show_add_agenda"]:
            
                sub_col1 = st.container()

                if st.session_state["show_agenda"]:
                    csv1 = "data/csvs/my_agenda.csv"
                    show_csv_interactive(csv1)

                    st.text("Change csv")
                    edit_csv(csv1)                    

                elif st.session_state["check_sources"]:
                    st.dataframe(df_piges)

                else:
                    file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.text_area("My notes", value=content, height=700)
            
            
            if st.session_state["show_add_agenda"]:
            
                sub_col1, sub_col2 = st.columns([2, 1])

                with sub_col1:
                    file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.text_area("My notes", value=content, height=700)

                with sub_col2:
                    st.subheader("Add to agenda")
                    csv_file = "data/csvs/my_agenda.csv"
                    str_add_to_df(csv_file)


################### AGENDA ###################
                
elif main_menu == "Agenda":

    tab1, tab2, tab3 = st.tabs(["Agenda","Journal","Notebook"])

    with tab1:
        st.subheader("Agenda")

        decl_col1, decl_col2 = st.columns(
            [4,1],
            gap="small",
            vertical_alignment="top",
            border=True
        )

        # -------------------- ΔΕΞΙΑ ΣΤΗΛΗ (controls) --------------------
        with decl_col2:

            # Init session_state
            st.session_state.setdefault("left_panel_text", "")
            st.session_state.setdefault("left_panel_title", "")
            st.session_state.setdefault("selected_date", None)

            # Φόρτωση DataFrame
            df = load_txt_agenda_folder()

            if df.empty:
                st.warning("Δεν βρέθηκαν αποδελτιώσεις")
                st.stop()

            # Init selected_date
            if st.session_state.selected_date is None:
                st.session_state.selected_date = df["date"].max()

            st.text("Search by date")
            st.session_state.selected_date = st.date_input(
                "Επίλεξε ημερομηνία",
                value=st.session_state.selected_date,
                min_value=df["date"].min(),
                max_value=df["date"].max()
            )

            # ---- Last agenda ----
                        
            
            if st.button("Last agenda"):
                last_row = df.iloc[-1]
                st.session_state["left_panel_text"] = last_row["text"]
                st.session_state["left_panel_title"] = f"Τελευταία Αποδελτίωση: {last_row['date']}"
                st.session_state.selected_date = last_row["date"]


            # ---- Φόρτωση αποδελτίωσης για επιλεγμένη ημερομηνία ----
            result = df[df["date"] == st.session_state.selected_date]
            if not result.empty:
                st.session_state["left_panel_text"] = result.iloc[0]["text"]
                st.session_state["left_panel_title"] = f"Agenda {st.session_state.selected_date}"
            else:
                st.session_state["left_panel_text"] = ""
                st.session_state["left_panel_title"] = ""
                st.warning("Δεν υπάρχει αποδελτίωση για αυτή την ημερομηνία")

            st.markdown("---")
            @st.cache_data
            def read_docx(file):
                """Διαβάζει DOCX αρχείο και επιστρέφει κείμενο"""
                doc = Document(file)
                return '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])


            uploaded_file = st.file_uploader("Save to agenda folder", type=['docx'])

            if uploaded_file is not None:
                text_content = read_docx(uploaded_file)
                st.text_area("Περιεχόμενο DOCX", text_content, height=300)
                
                title = st.text_input("Add title yyyy-mm-dd")
                SAVE_FOLDER = Path("data/agenda")
                SAVE_FOLDER.mkdir(parents=True, exist_ok=True)

                # Αποθήκευση ως txt
                if st.button("Αποθήκευση ως TXT"):
                    if not title.strip():
                        st.error("❌ Ο τίτλος δεν μπορεί να είναι κενός")
                    else:
                        filename = f"{title.strip()}.txt"
                        save_path = SAVE_FOLDER / filename

                        with open(save_path, "w", encoding="utf-8") as f:
                            f.write(text_content)

                        st.success(f"✅ Αποθηκεύτηκε: {save_path}")

        # -------------------- ΑΡΙΣΤΕΡΗ ΣΤΗΛΗ (display) --------------------
        with decl_col1:
            
            if st.button("Δείξε df",key="main"):
                st.dataframe(df)
            
            if st.session_state["left_panel_text"]:
                st.subheader(st.session_state["left_panel_title"])
                st.text_area(
                    "",
                    st.session_state["left_panel_text"],
                    height=700
                )
            else:
                st.info("Επίλεξε μια ημερομηνία ή την 'Τελευταία Αποδελτίωση' στη δεξιά στήλη.")

    with tab2:
        st.subheader("Journal")


        # ---------- DB helper ----------
        def get_db():
            conn = sqlite3.connect("DBs/tasks.db", check_same_thread=False)
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_date DATE,
                    title TEXT,
                    description TEXT
                )
            """)
            conn.commit()
            return conn, c


        # ---------- SESSION STATE INIT ----------
        if "journal_view" not in st.session_state:
            st.session_state["journal_view"] = "today"   # today | programmed | week

        if "task_title" not in st.session_state:
            st.session_state["task_title"] = ""

        if "task_description" not in st.session_state:
            st.session_state["task_description"] = ""

        if "task_date" not in st.session_state:
            st.session_state["task_date"] = date.today()


        # ---------- TAB ----------
        with tab2:

            journal_col1, journal_col2 = st.columns(
                [4, 1],
                gap="small",
                vertical_alignment="top",
                border=True
            )

            conn, c = get_db()

            # ---------- RIGHT COLUMN (ACTIONS) ----------
            with journal_col2:

                if st.button("Today's tasks"):
                    st.session_state["journal_view"] = "today"

                if st.button("Programmed tasks"):
                    st.session_state["journal_view"] = "programmed"

                if st.button("This week"):
                    st.session_state["journal_view"] = "week"

                st.markdown("---")

                with st.expander("Add new task"):
                    with st.form("new_task_form"):
                        st.date_input(
                            "Date",
                            key="task_date"
                        )

                        st.text_input(
                            "Τίτλος",
                            key="task_title"
                        )

                        st.text_area(
                            "Περιγραφή",
                            key="task_description"
                        )

                        # Callback για να καθαρίζει το form μετά την υποβολή
                        def clear_form():
                            st.session_state["task_title"] = ""
                            st.session_state["task_description"] = ""
                            st.session_state["task_date"] = date.today()

                        # Υποβολή φόρμας με callback
                        submitted = st.form_submit_button("Αποθήκευση")

                        if submitted:
                            if st.session_state["task_title"].strip():
                                c.execute(
                                    "INSERT INTO tasks (task_date, title, description) VALUES (?, ?, ?)",
                                    (
                                        st.session_state["task_date"],
                                        st.session_state["task_title"],
                                        st.session_state["task_description"]
                                    )
                                )
                                conn.commit()

                                st.success("✅ Το task αποθηκεύτηκε!")
                            else:
                                st.warning("Δώσε τουλάχιστον τίτλο.")

    # ---------- LEFT COLUMN (VIEW) ----------
    with journal_col1:

        view = st.session_state["journal_view"]

        # ---- TODAY ----
        if view == "today":
            today = date.today()

            c.execute("""
                SELECT task_date, title, description
                FROM tasks
                WHERE DATE(task_date) = DATE(?)
                ORDER BY id
            """, (today,))
            rows = c.fetchall()

            st.subheader("📅 Today's tasks")

            if rows:
                for r in rows:
                    task_dt = date.fromisoformat(r[0])
                    st.markdown(f"**{task_dt.strftime('%d/%m/%Y')}** – **{r[1]}**: {r[2]}")
            else:
                st.info("Δεν υπάρχουν tasks για σήμερα.")

        # ---- PROGRAMMED ----
        elif view == "programmed":
            st.subheader("📋 Programmed tasks")

            view_date = st.date_input(
                "Εμφάνιση tasks για:",
                value=date.today(),
                key="view_programmed_date"
            )

            c.execute(
                "SELECT task_date, title, description FROM tasks WHERE DATE(task_date) = DATE(?)",
                (view_date,)
            )
            rows = c.fetchall()

            if rows:
                for r in rows:
                    task_dt = date.fromisoformat(r[0])
                    st.markdown(f"**{task_dt.strftime('%d/%m/%Y')}** – **{r[1]}**: {r[2]}")
            else:
                st.info("Δεν υπάρχουν tasks για αυτή την ημερομηνία.")

        # ---- WEEK ----
        elif view == "week":
            st.subheader("📆 This week")

            today = date.today()
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)

            c.execute("""
                SELECT task_date, title, description
                FROM tasks
                WHERE DATE(task_date) BETWEEN DATE(?) AND DATE(?)
                ORDER BY DATE(task_date)
            """, (monday, sunday))
            rows = c.fetchall()

            if rows:
                for r in rows:
                    task_dt = date.fromisoformat(r[0])
                    st.markdown(f"**{task_dt.strftime('%d/%m/%Y')}** – **{r[1]}**: {r[2]}")
            else:
                st.info("Δεν υπάρχουν tasks για αυτή την εβδομάδα.")


        with tab3:

            st.subheader("Notebook")

            if "notebook_ready" not in st.session_state:
                st.session_state.notebook_ready = False
 
            if "notebook_txt" not in st.session_state:
                st.session_state.notebook_txt = True

            notebook_col1, notebook_col2 = st.columns(
                [4,1],
                gap="small",
                vertical_alignment="top",
                border=True
            )

            with notebook_col1:

                if st.session_state.notebook_txt:
                    text_for_agenda = st.text_area("Βάλε το κείμενο εδώ:", height=200)

                if st.session_state.notebook_ready:
                    st.session_state.notebook_txt = False

                    with open("data/texts/σημειώσεις.txt", "r", encoding="utf-8") as f:
                        notes = f.read()

                    st.text_area("Σημειώσεις", notes, height=300)


            with notebook_col2:
                if st.button("Show notes"):
                    st.session_state.notebook_ready = True
                    st.session_state.notebook_txt = False

                    with open("data/texts/σημειώσεις.txt", "r", encoding="utf-8") as f:
                        f.read()
                    

                if st.button("Add texts to notes"):
                    add_text_shmeioseis_streamlit(text_for_agenda)
                
                st.markdown("---")

                file_name = st.text_input("Δώστε όνομα στο αρχείο (χωρίς κατάληξη)")
                if st.button("Save text to a new file",help="Enter file name to the field above"):
                    create_or_append_txt_streamlit(file_name,text_for_agenda)


################### DATABASES ###################
                

elif main_menu == "Databases":

    if "show_db_creator" not in st.session_state:
        st.session_state.show_db_creator = False
                
    if "show_db_options" not in st.session_state:
        st.session_state.show_db_options = False

    if "titles_menu" not in st.session_state:
        st.session_state.titles_menu = "Τίτλοι γεωπολιτικά"
    
    st.set_page_config(layout="wide")
    st.subheader("Multi-Database Manager")

    tab_labels = list(DATABASES.keys()) + ["Διαχείριση ΒΔ"]

    tabs = st.tabs(tab_labels)

    for tab, label in zip(tabs, tab_labels):
        with tab:
            if label in DATABASES:
                cfg = DATABASES[label]
                sql_render_db_manager(
                    db_path=cfg["path"],
                    read_only=cfg["read_only"],
                    key=label.replace(" ", "_")
                )
            elif label == "Διαχείριση ΒΔ":
                

                db_col1, db_col2 = st.columns(
                [4,1],
                gap="small",
                vertical_alignment="top",
                border=True
               )
                
                with db_col2:
                    if st.button("Scrap Titles",help="Scraps specific sites with specific words for news DB"):
                        scr_from_news_to_db_and_persons3_streamlit()

                    if st.button("Open main DB filters", help="Basic filters for News DBs"):
                        st.session_state.show_db_creator = False
                        st.session_state.show_db_options = True

                    st.markdown("---")

                    if st.button("Create new DB",help="Creates a new DB in DBs folder"):
                        st.session_state.show_db_creator = True
                        st.session_state.show_db_options = False
                    
                    

                        

                with db_col1:
                    if st.session_state.get("show_db_creator"):
                        streamlit_sqlite_creator(key="creator_main")

                    if st.session_state.get("show_db_options"):
                        
                        titles_menu = st.selectbox(
                            "See Categories in News DB",
                            [
                                "Τίτλοι γεωπολιτικά",
                                "Τίτλοι πολιτική",
                                "Τίτλοι οικονομία",
                                "Ψάξε σε τίτλους"
                            ],
                            key="titles_menu"
                        )

                        choice = st.session_state.titles_menu

                        if choice == "Τίτλοι γεωπολιτικά":
                            read_titles_geopol_streamlit()
                        elif choice == "Τίτλοι πολιτική":
                            read_titles_pol_streamlit()
                        elif choice == "Τίτλοι οικονομία":
                            read_titles_economy_streamlit()
                        elif choice == "Ψάξε σε τίτλους":
                            sq_search_to_titles_streamlit2()



################### NEWSROOM TOOLS ###################


elif main_menu == "NewsRoom Tools":

    newsroom_tab1, newsroom_tab2,newsroom_tab3,newsroom_tab4,newsroom_tab5,newsroom_tab6 = st.tabs(["Editor","Newsroom tools","Transcribe","OCR","From one to another","All the rest"])

    with newsroom_tab1:
        main_writing_area()

    with newsroom_tab2:
        st.subheader("Newsroom Tools")
        
        if "newsroom_mode" not in st.session_state:
            st.session_state.newsroom_mode = None

        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)
        
        with col2:

            if st.button("Suggest Title"):
                st.session_state.newsroom_mode = "title"

            if st.button("Summary"):
                st.session_state.newsroom_mode = "summary"

            if st.button("Keypoints",key="With DeepSeek"):
                st.session_state.newsroom_mode = "keypoints"

            if st.button("Spelling correction"):
                st.session_state.newsroom_mode = "fix"

            if st.button("From transcription to reportage"):
                st.session_state.newsroom_mode = "report"

            if st.button("Rephrase the news"):
                st.session_state.newsroom_mode = "rewrite"

            if st.button("Translation from English"):
                st.session_state.newsroom_mode = "translate"

        
        with col1:
            mode = st.session_state.newsroom_mode

            # Text area που ενημερώνει το session_state αυτόματα
            user_text = st.text_area("Insert your text here:", height=200, key='user_text')

            if mode == "title":
                tr_generate_title_streamlit(user_text)

            elif mode == "summary":
                tr_generate_summary_streamlit(user_text)

            elif mode == "keypoints":
                gpt_deepseek_vasika_simeia(user_text)

            elif mode == "fix":
                gpt_mistral_diorthosi_streamlit(user_text)

            elif mode == "report":
                gpt_mistral_plagios_streamlit(user_text)

            elif mode == "rewrite":
                gpt_mistral_alli_diatiposi_streamlit(user_text)

            elif mode == "translate":
                translate_el_streamlit2(user_text)

    with newsroom_tab3:
        st.subheader("Transcription Tools")
        
        if "newsroom_transcribe" not in st.session_state:
            st.session_state.newsroom_transcribe = None

        trans_col1, trans_col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

        with trans_col2:
            url = st.text_input("Please enter YouTube URL: ")

            if st.button("Transcribe from youtube"):
                st.session_state.newsroom_transcribe = "from_yt"
            
            st.markdown("---")

            uploaded_mp3 = st.file_uploader(
                "Upload MP3 for transcribe",
                type=["mp3"]
            )
            if st.button("Trancription from mp3"):
                st.session_state.newsroom_transcribe = "from_mp3"
                
            
            st.markdown("---")

            st.link_button("Youtube to Transcript",
                           "https://youtubetotranscript.com",
                           help="Opens external transciption app")
                
        
        with trans_col1:
            mode_transcribe = st.session_state.newsroom_transcribe

            if mode_transcribe == "from_yt":
                transcribe_youtube_streamlit(url)

            elif mode_transcribe == "from_mp3":
                transcribe_mp3_streamlit2(uploaded_mp3)


    with newsroom_tab4:    

        st.subheader("OCR")

        if "ocr_mode" not in st.session_state:
            st.session_state.ocr_mode = "off"

        ocr_col1, ocr_col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

        with ocr_col2:

            uploaded_photo = st.file_uploader(
            "Επέλεξε ένα αρχείο εικόνας για OCR",
            type=["jpg", "png"]  # αν θες μόνο εικόνες
            )
            if st.button("OCR από εικόνα"):
                if uploaded_photo is None:
                    st.warning("⚠️ Ανέβασε πρώτα εικόνα")
                else:
                    st.session_state.ocr_mode = "on"
                    
        with ocr_col1:
            
            if uploaded_photo is not None:
                st.image(uploaded_photo)

            if st.session_state.ocr_mode == "on" and uploaded_photo is not None:
                ocr_reader_streamlit(uploaded_photo)


    with newsroom_tab5:

        st.subheader("From One to Another Tools")

        main_one_to_another()

    
    
    with newsroom_tab6:

        st.subheader("All the rest")

        st.link_button("Βγάλε μπούσουλα", 
            "https://bousoulas.streamlit.app")
        
################### ECONOMY TOOLS ###################

elif main_menu == "Economy Tools":
    
    econ_tab1, econ_tab2, econ_tab3, econ_tab4, econ_tab5, econ_tab6 = st.tabs(
        ["Working Area","Open Pdfs","Data","Charts","Tools","Dictionaries"])
    
    with econ_tab1:
        st.subheader("Working Area")
        
        if "economy" not in st.session_state:
            st.session_state["economy"] = None
        

        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

        with col2:
            
            file_type = st.radio("Choose what to open",
                                 ["CSVs","Charts","Pdfs"],index=None)
            
            if file_type == "CSVs":
                st.session_state["economy"] = "csv"
            elif file_type == "Charts":
                st.session_state["economy"] = "chart"
            elif file_type == "Pdfs":
                st.session_state["economy"] = "pdf"
        
        with col1:
            with st.expander("Open file",expanded=False):

                if st.session_state["economy"] == "csv":
                    open_file_from_folder("data/economy_files/economy_csvs")
                elif st.session_state["economy"] == "chart":
                    open_file_from_folder("data/economy_files/economy_images")
                elif st.session_state["economy"] == "pdf":
                    open_file_from_folder("data/economy_files/economy_pdfs")

            economy_text = st.text_area("Keep your notes here",height=400)
            
            ps_col1, ps_col2 = st.columns(2)

            with ps_col1:
                if st.button("Save note",key="ec_1"):
                    file_path = "data/economy_files/economy_notes.txt"
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(economy_text)
                    st.success("Text saved on economy notes!")
            
            with ps_col2:
                if st.button("Clear note",key="ec_2"):
                    file_path = "data/economy_files/economy_notes.txt"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write("")
                    st.success("Νotes cleared!")

    
    with econ_tab2:
        st.subheader("Open pdf")

        col1, col2 = st.columns([4, 1], gap="small", vertical_alignment="top", border=True)

        folder_path = "data/economy_files/economy_pdfs"

        folder_path = "data/economy_files/economy_pdfs"

        with col2:
            st.subheader("📂 Επιλογή Αρχείου")
            
            # Επιβεβαιώνει ότι ο φάκελος υπάρχει
            if not os.path.exists(folder_path):
                st.error(f"Ο φάκελος δεν βρέθηκε: {folder_path}")
                st.info("Δημιουργία φακέλου...")
                os.makedirs(folder_path, exist_ok=True)
                files = []
            else:
                files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
            
            if not files:
                st.warning("Δεν βρέθηκαν αρχεία PDF στον φάκελο")
                selected_file = None
            else:
                selected_file = st.selectbox("Επιλογή αρχείου PDF", files, index=0)
            
            st.markdown("---")
            
            # ΚΟΥΜΠΙΑ ΕΞΑΓΩΓΗΣ
            st.subheader("🛠️ Εξαγωγή Περιεχομένου")
            
            if selected_file:
                file_path = os.path.join(folder_path, selected_file)
                
                # Κουμπί εξαγωγής πινάκων
                if st.button("📊 Εξαγωγή Πινάκων", use_container_width=True):
                    with st.spinner("Αναζήτηση πινάκων..."):
                        tables = extract_tables_from_pdf(file_path)
                        
                        if tables:
                            st.success(f"Βρέθηκαν {len(tables)} πίνακες/εικόνες")
                            
                            for i, table_data in enumerate(tables):
                                with st.expander(f"Πίνακας {i+1} - Σελίδα {table_data['page']}"):
                                    if 'table' in table_data:
                                        # Αν είναι δομημένος πίνακας
                                        df = pd.DataFrame(table_data['table'])
                                        st.dataframe(df, use_container_width=True)
                                        
                                        # Λήψη ως CSV
                                        csv = df.to_csv(index=False).encode('utf-8')
                                        st.download_button(
                                            label=f"📥 Λήψη Πίνακα {i+1} ως CSV",
                                            data=csv,
                                            file_name=f"table_{i+1}_page_{table_data['page']}.csv",
                                            mime="text/csv",
                                            key=f"csv_{i}"
                                        )
                                    elif 'image' in table_data:
                                        # Αν είναι εικόνα πίνακα
                                        st.image(table_data['image'], caption=f"Εικόνα πίνακα - Σελίδα {table_data['page']}")
                        else:
                            st.warning("Δεν βρέθηκαν πίνακες στο PDF")
                
                # Κουμπί εξαγωγής εικόνων
                if st.button("🖼️ Εξαγωγή Εικόνων", use_container_width=True):
                    with st.spinner("Εξαγωγή εικόνων..."):
                        images = extract_images_from_pdf(file_path)
                        
                        if images:
                            st.success(f"Βρέθηκαν {len(images)} εικόνες")
                            
                            # Ομαδοποίηση ανά σελίδα
                            from collections import defaultdict
                            images_by_page = defaultdict(list)
                            
                            for img in images:
                                images_by_page[img['page']].append(img)
                            
                            for page_num, page_images in images_by_page.items():
                                with st.expander(f"Σελίδα {page_num} ({len(page_images)} εικόνες)"):
                                    cols = st.columns(2)
                                    for idx, img in enumerate(page_images):
                                        col = cols[idx % 2]
                                        with col:
                                            pil_image = Image.open(io.BytesIO(img['image_bytes']))
                                            col.image(pil_image, caption=f"Εικόνα {img['index']+1}")
                                            
                                            # Λήψη εικόνας
                                            st.download_button(
                                                label=f"📥 Λήψη",
                                                data=img['image_bytes'],
                                                file_name=f"page_{page_num}_img_{img['index']+1}.{img['format']}",
                                                mime=f"image/{img['format']}",
                                                key=f"img_{page_num}_{idx}"
                                            )
                        else:
                            st.warning("Δεν βρέθηκαν εικόνες στο PDF")
            
            st.markdown("---")
            
            # ΣΗΜΕΙΩΣΕΙΣ ΧΡΗΣΤΗ
            st.subheader("📝 Σημειώσεις")
            notes = st.text_area("Οι σημειώσεις σας:", height=200, label_visibility="collapsed")

        with col1:
    #   if selected_file:

            file_path = os.path.join(folder_path, selected_file)
            
            # ΡΥΘΜΙΣΕΙΣ ZOOM
            st.subheader("📄 Προβολή PDF")

            try:
                with open(file_path, "rb") as f:
                    pdf_bytes = f.read()
                base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                
                st.markdown(
                    f'''
                    <div style="
                        width: 100%;
                        height: 800px;
                        position: relative;
                        overflow: hidden;
                    ">
                        <iframe 
                            src="data:application/pdf;base64,{base64_pdf}#view=FitH&zoom=300" 
                            style="
                                position: absolute;
                                top: 0;
                                left: 0;
                                width: 100%;
                                height: 100%;
                                border: none;
                            "
                            title="PDF Document"
                        ></iframe>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Σφάλμα φόρτωσης PDF: {e}")
            
            # ΚΕΙΜΕΝΟ ΑΝΑ ΣΕΛΙΔΑ (ΜΕ SELECTBOX)
            st.markdown("---")
            st.subheader("📖 Κείμενο ανά Σελίδα")
            
            # Αριθμός σελίδων
            try:
                doc = fitz.open(file_path)
                total_pages = len(doc)
                doc.close()
                
                if total_pages > 0:
                    # Selectbox για επιλογή σελίδας
                    page_options = [f"Σελίδα {i+1}" for i in range(total_pages)]
                    selected_page_label = st.selectbox(
                        "Επιλέξτε σελίδα:",
                        page_options,
                        index=0
                    )
                    
                    # Εξαγωγή αριθμού σελίδας
                    selected_page_num = int(selected_page_label.split()[-1]) - 1
                    
                    # Εμφάνιση κειμένου επιλεγμένης σελίδας
                    doc = fitz.open(file_path)
                    page = doc[selected_page_num]
                    page_text = page.get_text()
                    doc.close()
                    
                    if page_text.strip():
                        st.text_area(
                            f"Κείμενο {selected_page_label}",
                            page_text,
                            height=300,
                            key=f"page_{selected_page_num}"
                        )
                        
                        # Κουμπί λήψης για συγκεκριμένη σελίδα
                        st.download_button(
                            label=f"📥 Λήψη κειμένου {selected_page_label}",
                            data=page_text,
                            file_name=f"{os.path.splitext(selected_file)[0]}_page_{selected_page_num+1}.txt",
                            mime="text/plain",
                            key=f"download_page_{selected_page_num}"
                        )
                    else:
                        st.info("Αυτή η σελίδα δεν περιέχει κείμενο")
                else:
                    st.warning("Το PDF δεν έχει σελίδες")
                    
            except Exception as e:
                st.error(f"Σφάλμα ανάγνωσης σελίδων: {e}")
            
            # ΠΛΗΡΕΣ ΚΕΙΜΕΝΟ (ΟΠΤΙΚΑ)
            st.markdown("---")
            with st.expander("📄 Πλήρες κείμενο PDF (όλες οι σελίδες)"):
                if st.button("Εξαγωγή πλήρους κειμένου"):
                    with st.spinner("Εξαγωγή κειμένου..."):
                        full_text = pdf_open_streamlit(file_path)
                        
                        if full_text:
                            st.text_area("Πλήρες κείμενο", full_text, height=400)
                            
                            st.download_button(
                                label="📥 Λήψη πλήρους κειμένου",
                                data=full_text,
                                file_name=f"{os.path.splitext(selected_file)[0]}_full.txt",
                                mime="text/plain",
                                key="download_full"
                            )
                        else:
                            st.warning("Δεν βρέθηκε κείμενο στο PDF")

    
    with econ_tab3:
        st.subheader("Data")

        if "data" not in st.session_state:
            st.session_state["data"] = "companies"

        folder = "data/economy_files/economy_ymls"

        
        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)


        with col1:
            
            if st.session_state["data"] == "yaml":
                yaml_obj, filepath = load_yaml_files(folder)

                st.divider()
                edit_yaml_data(yaml_obj["data"])

                if st.button("💾 Save"):
                    with open(filepath, "w", encoding="utf-8") as f:
                        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
                    st.success("Saved ✅")
            
            elif st.session_state["data"] == "new_yaml":
                
                new_yaml4(folder)

                with st.expander("YAML Cheet Sheet",expanded=False):
                    st.write("""
                                Ορίστε ένα **πολύ σύντομο YAML cheat sheet** 🚀

                                ---

                                ## YAML Cheat Sheet (ultra-short)

                                ### 1️⃣ Βασικό: key → value

                                ```yaml
                                topic: energy
                                year: 2022
                                ```

                                ---

                                ### 2️⃣ Εσοχές (ΜΟΝΟ spaces)

                                ```yaml
                                parent:
                                child: value
                                ```

                                ---

                                ### 3️⃣ Λίστα

                                ```yaml
                                items:
                                - one
                                - two
                                ```

                                ---

                                ### 4️⃣ Λίστα αντικειμένων

                                ```yaml
                                companies:
                                - name: Mytilineos
                                    profit: 184
                                ```

                                ---

                                ### 5️⃣ Πολλές γραμμές κείμενο

                                ```yaml
                                notes: |
                                Πρώτη γραμμή
                                Δεύτερη γραμμή
                                ```

                                ---

                                ### 6️⃣ Αριθμοί με μονάδες (σωστός τρόπος)

                                ```yaml
                                value: 500
                                unit: billion_eur
                                ```

                                ---

                                ### 7️⃣ Ημερομηνία

                                ```yaml
                                date: 2022-09-22
                                ```

                                ---

                                ### 8️⃣ Σχόλια

                                ```yaml
                                # Αυτό είναι σχόλιο
                                ```

                                ---

                                ### 9️⃣ Κανόνες naming

                                ```yaml
                                snake_case
                                αγγλικά
                                σταθερά keys
                                ```

                                ---

                                ### 🔟 Golden rule

                                > **Αν δεν μπορείς να το φιλτράρεις / βρεις μετά, δεν είναι καλό YAML.**

                                ---

                                Αν θες, στο επόμενο μήνυμα μπορώ να σου το κάνω **print-friendly PDF** ή **ένα έτοιμο template για όλα τα economy αρχεία σου**.

                                
                                """)

            elif st.session_state["data"] == "search":
                query = st.text_input("🔍 Αναζήτηση στο περιεχόμενο (data)")

                if query:
                    results = search_in_json_folder(folder, query)

                    if results:
                        for r in results:
                            st.markdown(f"""
                            **📄 {r['file']}**  
                            • `{r['location']}`  
                            • `{r['value']}`
                            """)
                    else:
                        st.info("Δεν βρέθηκαν αποτελέσματα")
                
            elif st.session_state["data"] == "companies":

                df_companies = pd.read_csv(
                    "data/csvs/companies.csv",
                    sep="\t",
                    engine="python",
                    encoding="utf-8-sig",
                    quotechar='"',
                    header=0
                )

                st.dataframe(df_companies)

                if st.button("Financial.gr"):
                    webbrowser.open("https://financials.gr")
                if st.button("GEMH data"):
                    webbrowser.open("https://publicity.businessportal.gr")
                
            elif st.session_state["data"] == "map":
                st.components.v1.iframe(
                    "https://www.google.com/maps/d/u/0/edit?mid=1FKEhsE8UuSNjuhtBRKIiDGZ82S1vENQ&usp=sharing",
                    height = 800,
                    scrolling = True
                )

            
        
        with col2:

            if st.button("Show yaml",help="Open yaml notes"):
                st.session_state["data"] = "yaml"

            if st.button("New Yaml",help="Creates new yaml"):
                st.session_state["data"] = "new_yaml"
            
            if st.button("Search jsons",help="Search in json files"):
                st.session_state["data"] = "search"
            
            st.markdown("---")

            if st.button("Show companies",help="See a df with data for main companies"):
                st.session_state["data"] = "companies"
            
            st.markdown("---")

            if st.button("Map test", help= "Shows a map with major companies"):
                st.session_state["data"] = "map"
            
            st.markdown("---")

            


    with econ_tab4:
            st.subheader("Charts")

            if "charts" not in st.session_state:
                st.session_state["charts"] = "make_chart"
            
            col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

            with col1:

                if st.session_state["charts"] == "excel":
                    uploaded_file = st.file_uploader("Ανέβασε ένα αρχείο Excel ή csv", type=["xlsx","csv"])
                    pandas_show_df(uploaded_file)

                elif st.session_state["charts"] == "open":
                    search_images2()
                
                elif st.session_state["charts"] == "make_chart":
                    dataframe_explorer("data/economy_files/economy_csvs")


            with col2: 

                if st.button("make a chart"):
                    st.session_state["charts"] = "make_chart"

                if st.button("Διάβασε ένα excel/csv"):
                    st.session_state["charts"] = "excel"

                if st.button("Open Charts"):
                    st.session_state["charts"] = "open"

                


    with econ_tab5:
            st.subheader("Tools")

            if "economy_tools" not in st.session_state:
                st.session_state["economy_tools"] = None
            
            col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

        
            with col1:

                text_input = st.text_area("Please enter your text here")

                if st.session_state["economy_tools"] == "summary":
                    gpt_mistral_oikonomia_streamlit(text_input)
                elif st.session_state["economy_tools"] == "dictionary":
                    lex_oikonomikon(text_input)

            with col2:

                if st.button("Financial summary",help="Codifies basic financial data with Mistral"):
                    st.session_state["economy_tools"] = "summary"
            
                if st.button("Dictionary of economic terms",help="connects economic concepts in the text with an external dictionary of economic terms"):
                    st.session_state["economy_tools"] = "dictionary"


            
    with econ_tab6:
            st.subheader("Dictionaries")
            
            col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True)

########################


elif main_menu == "NLP":

    

    user_text = st.text_area("Βάλτε κείμενο εδώ", height=200)

    NLP_menu = option_menu(
        "NLP Menu", 
        ["NER", "Λεξικά"])

    if NLP_menu == "NER":
        if st.button("Πρόσωπα και Οργανισμοί"):
            if user_text.strip():
                results = nlp_spacy_ner_grouped_entities(user_text)

                st.subheader("Αποτελέσματα:")
                for label, ents in results.items():
                    st.write(f"**{label}**: {', '.join(ents)}")
            else:
                st.warning("Γράψε πρώτα κείμενο!")

        if st.button("Βρες ημερομηνίες"):
            extract_date_sentences(user_text)

        if st.button("Χάρτης"):
            scr_from_text_to_map_streamlit(user_text)

    elif NLP_menu == "Λεξικά":
        if st.button("Διασύνδεση με γεωγραφικούς όρους (semantics)"):
            lex_semantics_geo(user_text)
        
        if st.button("Προσθήκη links"):
            st.markdown("#### Τα link από δικό μου λεξικό")
            lex_add_links_exoteriko(user_text)
        
        if st.button("Custom βιβλιοθήκη"):
            lexiko_custom_show(user_text)
        
        if st.button("Λεξικό οικονομικών όρων"):
            lex_oikonomikon(user_text)



elif main_menu == "RAG":
    st.set_page_config(page_title="📄 PDF RAG με Mistral", page_icon="🤖")

    st.title("📄 PDF RAG Chatbot με Mistral")
    st.write("Ανέβασε ένα PDF και κάνε ερωτήσεις πάνω στο περιεχόμενό του!")

    uploaded_file = st.file_uploader("📤 Ανέβασε PDF", type="pdf")

    if uploaded_file is not None:
        pdf_to_rag_streamlit(uploaded_file)


elif main_menu == "GPTs":
    text = st.text_area("Κάνε εδώ την ερώτηση σου")
    if st.button("Ρώτα το DeepSeek"):
        gpt_deepseek_streamlit_short2(text)
    if st.button("Ρώτα το Mistral"):
        gpt_mistral_general_streamlit(text)


