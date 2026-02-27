
import re
import streamlit as st
import json
import html

def prosthese_links(keimeno, lexiko):
    for lexi, link in lexiko.items():
        pattern = re.compile(rf"\b{re.escape(lexi)}\b", re.IGNORECASE)
        
        safe_lexi = html.escape(lexi)
        
        if isinstance(link, dict) and 'url' in link:
            # Για URLs από το JSON
            replacement = f"[{safe_lexi}]({link['url']})"
        elif isinstance(link, str) and link.startswith("http"):
            replacement = f"[{safe_lexi}]({link})"
        else:
            # Για περιγραφές
            if isinstance(link, dict):
                content = link.get('description', str(link))
            else:
                content = str(link)
            
            safe_content = html.escape(content)
            replacement = f"<span title='{safe_content}' style='color: blue; text-decoration: underline; cursor: help; border-bottom: 1px dotted blue;'>{safe_lexi}</span>"
        
        keimeno = pattern.sub(replacement, keimeno)
    return keimeno

# Φόρτωση του νέου λεξικού
try:
    with open("ellinikes_etaireies.json", "r", encoding="utf-8") as f:
        lexiko_etaireion = json.load(f)
except FileNotFoundError:
    st.error("Δε βρέθηκε το αρχείο ellinikes_etaireies.json")
    lexiko_etaireion = {}

def lex_add_links_etaireies(user_input):
    st.subheader("🏢 Παραπομπές σε Ελληνικές Εταιρείες")

    if st.button("🔗 Μετατροπή σε κείμενο με links"):
        if user_input.strip():
            linked_text = prosthese_links(user_input, lexiko_etaireion)
            st.markdown(linked_text, unsafe_allow_html=True)
        else:
            st.warning("Παρακαλώ γράψε ή επικόλλησε ένα κείμενο πρώτα.")

user_input = st.text_area("Βάλτε το κείμενο σας", height=150, 
                         placeholder="Γράψτε ένα κείμενο που αναφέρεται σε ελληνικές εταιρείες...")

lex_add_links_etaireies(user_input)

