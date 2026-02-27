import streamlit as st
import streamlit.components.v1 as components
import re
import json

def lexiko_custom_show(keimeno):
    try:
        with open("data/lexika/lexiko_custom.json", "r", encoding="utf-8") as f:
            lexiko = json.load(f)
    except FileNotFoundError:
        st.error("Δε βρέθηκε το αρχείο lexiko_custom.json")
        return
    except json.JSONDecodeError:
        st.error("Σφάλμα στην ανάγνωση του JSON αρχείου")
        return

    def highlight_terms(text, dictionary):
        for lexi in dictionary:
            pattern = re.compile(rf"\b{re.escape(lexi)}\b", re.IGNORECASE)
            text = pattern.sub(f"**{lexi}**", text)
        return text

   
    if not keimeno.strip():
        st.warning("Παρακαλώ εισάγετε κείμενο πρώτα")
        return
        
    # Επισήμανση όρων στο κύριο κείμενο
    highlighted_text = highlight_terms(keimeno, lexiko)
    st.markdown(highlighted_text)
    
    # Sidebar με ορισμούς
    st.sidebar.header("📖 Ορισμοί")
    
    # Βρες ποιοι όροι υπάρχουν στο κείμενο (πιο ακριβής έλεγχος)
    existing_terms = []
    for lexi in lexiko:
        pattern = re.compile(rf"\b{re.escape(lexi)}\b", re.IGNORECASE)
        if pattern.search(keimeno):
            existing_terms.append(lexi)
    
    if existing_terms:
        st.sidebar.write(f"Βρέθηκαν {len(existing_terms)} όροι:")
        for term in existing_terms:
            with st.sidebar.expander(f"**{term}**", expanded=True):
                st.write(lexiko[term])
    else:
        st.sidebar.info("Δεν βρέθηκαν όροι από το λεξικό στο κείμενο")

