
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


# ============================================================
# 📁 MODULE 01 — Εισαγωγή, Άνοιγμα Αρχείων, PDF, Pandas
# ============================================================
from mod_01_enter_open import (
    add_text_agenda_streamlit,
    add_text_shmeioseis_streamlit,
    create_or_append_txt_streamlit
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
    rn_sources_selector
)


# ============================================================
# 📁 MODULE 05 — SQL Databases
# ============================================================
from mod_05_sql import sq_search_to_titles_streamlit2
from mod_05_sql_streamlit import main_db_streamlit
from mod_05_other_dbs import (
    agenda_streamlit,
    search_agenda_date_streamlit,
    show_last_agenda_stream
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

# ============================================================
# 🔧 HELPERS ΓΙΑ ΠΗΓΕΣ
# ============================================================

def rizospastis_rss():
    with st.expander("Διάλεξε για Ριζοσπάστη", expanded=True):
        if st.button("Δες τις κυριότερες ειδήσεις"):
            feed_read_rizospastis_streamlit()
        if st.button("Δες την Άποψη"):
            rizos_apopsi()
        if st.button("Σώσε σε ΒΔ"):
            feed_to_R_db()
        if st.button("ΒΔ Ριζοσπάστης"):
            show_R_DB_streamlit()

# ============================================================
# ⚙️ CONFIG — ΠΗΓΕΣ
# ============================================================

SOURCES_MENU = {
    "Ριζοσπάστης - 902": "rizospastis",
    "Oικονομικές σελίδες": "economy",
    "Γενικά": "general",
    "Διεθνής Οικονομία": "global_economy",
    "Διεθνή": "international",
    "Παραπολιτικά": "parapolitika",
    "Βουλή": "vouli",
    "Ραδιόφωνα": "radios"
}

SUBMENUS = {

    "rizospastis": {
        "menu": [
            "Ριζοσπάστης_RSS",
            "Άνοιξε τον Ριζοσπάστη",
            "Άνοιξε τον 902",
            "902_feed"
        ],
        "actions": {
            "Ριζοσπάστης_RSS": rizospastis_rss,
            "Άνοιξε τον Ριζοσπάστη": lambda: webbrowser.open_new_tab("https://www.rizospastis.gr"),
            "Άνοιξε τον 902": lambda: webbrowser.open_new_tab("https://www.902.gr"),
            "902_feed": feed_read_902_streamlit
        }
    },

    "economy": {
        "menu": [
            "OT.gr",
            "Καθημερινή",
            "Ναυτεμπορική",
            "Capital"
        ],
        "actions": {
            "OT.gr": lambda: webbrowser.open_new_tab("https://www.ot.gr"),
            "Καθημερινή": lambda: webbrowser.open_new_tab("https://www.kathimerini.gr/economy/"),
            "Ναυτεμπορική": lambda: webbrowser.open_new_tab("https://www.naftemporiki.gr/finance/economy/"),
            "Capital": lambda: webbrowser.open_new_tab("https://www.capital.gr/oikonomia"),
        }

#        "auto": rn_economy_news_buttons
    },

    "general": {
        "auto": rn_show_general_news
    },

    "global_economy": {
        "auto": lambda: (
            rn_global_economy_news_buttons(),
            feed_google_news_streamlit()
        )
    },

    "international": {
        "auto": lambda: (
            rn_show_diethni_news(),
            rn_show_geopolitics_news(),
            rn_show_brics_news()
        )
    },

    "parapolitika": {
        "auto": read_parapolitika_all_streamlit
    },

    "vouli": {
        "buttons": {
            "Το πρόγραμμα της Βουλής": rn_vouli,
            "vouliwatch": lambda: webbrowser.open("https://vouliwatch.gr/news"),
            "Πρακτικά": lambda: webbrowser.open(
                "https://www.hellenicparliament.gr/Praktika/Synedriaseis-Olomeleias"
            )
        }
    },

    "radios": {
        "auto": rn_radios
    }
}

# ============================================================
# 🧭 RENDERER — ΠΗΓΕΣ
# ============================================================

def render_sources():
    main_choice = option_menu(
        "Πηγές",
        list(SOURCES_MENU.keys()),
        orientation="horizontal",
        key="sources_navbar"
    )

    section_key = SOURCES_MENU[main_choice]
    section = SUBMENUS.get(section_key)

    if not section:
        return

    # AUTO sections (μένουν ως έχουν)
    if "auto" in section:
        section["auto"]()
        return

    # MENU sections (ΔΕΝ εκτελούν άμεσα)
    if "menu" in section:
        choice = option_menu(
            "",
            section["menu"],
            orientation="horizontal",
            key=f"{section_key}_menu"
        )

        # ⬇️ ΕΔΩ ΑΛΛΑΖΕΙ ΤΟ ΣΗΜΑΝΤΙΚΟ
        st.session_state["pending_action"] = section["actions"].get(choice)

        if st.session_state.get("pending_action"):
            if st.button("Άνοιγμα"):
                st.session_state["pending_action"]()

    # BUTTON sections (ήδη σωστά)
    if "buttons" in section:
        for label, func in section["buttons"].items():
            if st.button(label):
                func()



# ********************* TEST AREA *********************



with st.sidebar:
    main_menu = option_menu(
        "Κύριο Μενού",
        [ 
         "Πρωτοσέλιδα", 
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



if main_menu == "Πρωτοσέλιδα":
        
        st.title("Πρωτοσέλιδα εφημερίδων")

        if st.button("Click for Frontpages"):
            webbrowser.open_new_tab("https://www.frontpages.gr")



elif main_menu == "Πηγές":
    

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8,  = st.tabs(["Ριζοσπάστης - 902",
                                "Global economy",
                                "General",
                                "Economy",
                                "International",
                                "Παραπολιτικά",
                                "Βουλή",
                                "Ραδιόφωνα"
                                ])

    with tab1:
        st.subheader("Rizospastis")
        col1, col2 = st.columns([3, 1])

        with col2:
        
            choiceR = st.selectbox("Rizos_choose",["Main articles","Opinion","Save to db","Rizos_DB"], index=0)

            st.button("Open Rizos")
        
        
        with col1:

            if choiceR == "Main articles":
                feed_read_rizospastis_streamlit()
            elif choiceR == "Opinion":
                rizos_apopsi()
            elif choiceR == "Save to db":
                feed_to_R_db()
            elif choiceR == "Rizos_DB":
                show_R_DB_streamlit()

    
    with tab2:
        
        global_cols1, global_cols2 = st.columns([3,1])

        with global_cols1:
            feed_google_news_streamlit()

        with global_cols2:
            st.text("Open one of these")
            rn_sources_selector()

    with tab3:

        general_cols1, general_cols2 = st.columns([3,1])

        with general_cols1:
            st.text("One of these")    
        
        with general_cols2:
            general_options = {

            "Πρώτο θέμα": "https://www.protothema.gr/",
            "in.gr": "https://www.in.gr/",
            "CNN": "https://www.cnn.gr/",
            "Ναυτεμπορική": "https://www.naftemporiki.gr/",
            "Capital": "https://www.capital.gr/",
            "Καθημερινή": "https://www.kathimerini.gr/",
            "ΟΤ": "https://www.ot.gr/",
            "ΕφΣυν":  "https://www.efsyn.gr/",
            "Ieidiseis": "https://www.ieidiseis.gr/",
            "Mono_news": "https://www.mononews.gr/"
    
            }
    

            selected_source = st.selectbox(
                "Γενικές ειδήσεις",
                list(general_options.keys()),
                index=0
            )

            st.link_button(
                "Άνοιγμα πηγής",
                general_options[selected_source]
            )

    
    
    render_sources()
    

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


