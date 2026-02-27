######## 
########  Περίοδος ενασχόλησης 25 - 28/12/2025
######## Τι άλλαξε: αρχίζει νέο layout με tabs και στήλες 
######## Μπήκαν i - frames για να δείχνουν ζωντανές ιστοσελίδες
######## Μπήκε σημειωματάριο στη δεξιά στήλη που σώζει σε ένα κοινό αρχείο 
######## Δημιουργήθηκε (κοινό λεξικό json για τις Πηγές και διαφορετικά φίλτρα με τα οποία μπορεί να ψάξει ο χρήστης)
######## ? υπάρχουν ζητήματα σχετικά με το πώς κατηγοριοποιούνται οι πηγές



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




# ============================================================
# 📁 MODULE 01 — Εισαγωγή, Άνοιγμα Αρχείων, PDF, Pandas
# ============================================================
from mod_01_enter_open import (
    add_text_agenda_streamlit,
    add_text_shmeioseis_streamlit,
    create_or_append_txt_streamlit,
    
)

from mod_01_pdf import pdf_open_streamlit
from mod_01_pandas_charts import pandas_show_df


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




# ********************* TEST AREA *********************



with st.sidebar:
    main_menu = option_menu(
        "Κύριο Μενού",
        [ 
         "Πηγές", 
         "Αποδελτίωση", 
         "ΒΔ Ειδήσεων",
         "Scrap Τίτλοι",
        "NewsRoom Tools",
        "Economy Tools",
          "NLP", "Απομαγνητοφώνηση κτλ", "Charts", "RAG", "GPTs", "Σημειωματάριο", "Ημερολόγιο"],
        icons=["house", "newspaper", "globe", "calendar-event","database","database","tools","tools", "tools","mic","bar-chart", "robot", "globe","journal-text","calendar"],
        menu_icon="cast",
        default_index=0,
        )


if main_menu == "Πηγές":
    
    df_piges = rn_load_sources()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10  = st.tabs([
                                "Πρωτοσέλιδα",
                                "Ριζοσπάστης - 902",
                                "News",
                                "Economy",
                                "Global economy",
                                "International",
                                "Παραπολιτικά",
                                "Parliament - Government",
                                "Ραδιόφωνα",
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
        col1, col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

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

                elif choice_bouli == "vouliwatch":
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
            elif choice_bouli == "vouliwatch":
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
        st.subheader("Radio")
        general_cols1, general_cols2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")

    with tab10: 
        st.subheader("Notes")
        
        notes_col1, notes_col2 = st.columns(([4,1]), gap="small", vertical_alignment="top", border=True, width="stretch")
        
        with notes_col2:
            
            if "check sources" not in st.session_state:
                st.session_state["check_sources"] = False

            if st.button("Check notes"):
                st.session_state["check_sources"] = False

            if st.button("Clear notes"):
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "w", encoding="utf-8") as f:
                    content = f.write("----- New notes -----")
            
            st.markdown("---")

            if st.button("Check sources"):
                st.session_state["check_sources"] = True
            
    
        
        with notes_col1:

            if not st.session_state["check_sources"]:
                file_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/texts/Σημειώσεις_νεα.txt"
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.text_area("My notes", value=content, height=700)

            if st.session_state["check_sources"]:
                st.dataframe(df_piges)

    
                
elif main_menu == "Αποδελτίωση":

    tab1, tab2, tab3 = st.tabs(["Αποδελτίωση","Σημειωματάριο","Ημερολόγιο"])

    with tab1:
        st.subheader("Declensions")

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
                st.session_state.selected_date = df["date"].min()

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
            

                

        
    
    
########################
            
elif main_menu == "ΒΔ Ειδήσεων":
    main_db_streamlit()

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


elif main_menu == "NewsRoom Tools":
    user_text = st.text_area("Βάλε το κείμενο εδώ:", height=200)

    if st.button("Πρότεινε τίτλο"):
        tr_generate_title_streamlit(user_text)
    
    if st.button("Περίληψη"):
        tr_generate_summary_streamlit(user_text)

    if st.button("Βασικά σημεία (DeepSeek)"):
        gpt_deepseek_vasika_simeia(user_text)

    if st.button("Διόρθωσε το κείμενο"):
        gpt_mistral_diorthosi_streamlit(user_text)

    if st.button("Από απομαγνητοφώνηση σε ρεπορτάζ"):
        gpt_mistral_plagios_streamlit(user_text)

    if st.button("Επαναδιατύπωσε την είδηση"):
        gpt_mistral_alli_diatiposi_streamlit(user_text)

    if st.button("Από ανακοίνωση ρεπορτάζ"):
        gpt_mistral_anakoinosi_streamlit(user_text)
    

    if st.button("Μετάφραση από αγγλικά"):
        translate_el_streamlit2(user_text)
    

elif main_menu == "Economy Tools":
    text_input = st.text_area("Βάλτε το κείμενο σας εδώ")
    if st.button("Οικονομική περίληψη"):
        gpt_mistral_oikonomia_streamlit(text_input)
    
    st.write("-------------")
    uploaded_file = st.file_uploader("Ανέβασε ένα αρχείο Excel ή csv", type=["xlsx","csv"])

    if st.button("Διάβασε ένα excel/csv"):
        pandas_show_df(uploaded_file)

    if st.button("Λεξικό Οικονομικών Όρων"):
        lex_oikonomikon(text_input)

elif main_menu == "Charts":
        search_images2()


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


elif main_menu == "Απομαγνητοφώνηση κτλ":
    
    url = st.text_input("Please enter YouTube URL: ")

    if st.button("Απομαγνητοφώνηση από youtube"):
        transcribe_youtube_streamlit(url)
    
    st.write("----------")

    if st.button("Βγάλε μπούσουλα"):
        webbrowser.open("https://bousoulas.streamlit.app")

    st.write("----------")

    uploaded = st.file_uploader(
            "Επέλεξε ένα αρχείο MP3 για απομαγνητοφώνηση",
            type=["mp3"]
        )
    if st.button("Aπομαγνητοφώνηση από mp3"):
        transcribe_mp3_streamlit2(uploaded)

    st.write("----------")

    uploaded_photo = st.file_uploader(
    "Επέλεξε ένα αρχείο εικόνας για OCR",
    type=["jpg", "png"]  # αν θες μόνο εικόνες
    )
    if st.button("OCR από εικόνα"):
        ocr_reader_streamlit(uploaded_photo)

    st.write("----------")

    pdf = st.file_uploader("Ανέβασε ένα PDF αρχείο", type=["pdf"])

    if st.button("Pdf to txt"):
        pdf_open_streamlit(pdf)

elif main_menu == "RAG":
    st.set_page_config(page_title="📄 PDF RAG με Mistral", page_icon="🤖")

    st.title("📄 PDF RAG Chatbot με Mistral")
    st.write("Ανέβασε ένα PDF και κάνε ερωτήσεις πάνω στο περιεχόμενό του!")

    uploaded_file = st.file_uploader("📤 Ανέβασε PDF", type="pdf")

    pdf_to_rag_streamlit(uploaded_file)


elif main_menu == "GPTs":
    text = st.text_area("Κάνε εδώ την ερώτηση σου")
    if st.button("Ρώτα το DeepSeek"):
        gpt_deepseek_streamlit_short2(text)
    if st.button("Ρώτα το Mistral"):
        gpt_mistral_general_streamlit(text)


elif main_menu == "Σημειωματάριο":
        text_for_agenda = st.text_area("Βάλε το κείμενο εδώ:", height=200)
        if st.button("Πρόσθεσε το κείμενο στην ατζέντα"):
            add_text_agenda_streamlit(text_for_agenda)
        if st.button("Πρόσθεσε το κείμενο στις σημειώσεις"):
            add_text_shmeioseis_streamlit(text_for_agenda)
        
        file_name = st.text_input("Δώστε όνομα στο αρχείο (χωρίς κατάληξη)")
        if st.button("Σώσε σε ένα νέο κείμενο"):
            create_or_append_txt_streamlit(file_name,text_for_agenda)

elif main_menu == "Ημερολόγιο":
        imerologio()


