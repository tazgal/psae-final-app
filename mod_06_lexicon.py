import re
import streamlit as st
from unidecode import unidecode
import json
import unicodedata


# -----------------------
# Μετατροπή JSON-LD σε λεξικό
# -----------------------
def jsonld_to_lexicon(jsonld):
    lexicon = {}
    for entry in jsonld:
        labels = entry.get("http://www.w3.org/2004/02/skos/core#prefLabel", [])
        if labels:
            for label in labels:
                term = label.get("@value", "").strip()
                if term:
                    lexicon[term] = {"uri": entry["@id"]}
        else:
            # Αν δεν έχει label, παίρνουμε το τελευταίο κομμάτι του URI
            term = entry["@id"].rstrip("/").split("/")[-1]
            lexicon[term] = {"uri": entry["@id"]}
    return lexicon

# -----------------------
# Normalize ελληνικού κειμένου
# -----------------------
def normalize(text: str) -> str:
    """Αφαιρεί τόνους, κάνει lowercase"""
    return unidecode(text).lower()

def normalize_greek(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    return text

# -----------------------
# Εξαγωγή όρων
# -----------------------
def extract_terms(text, lexicon):
    terms_found = []
    norm_text = normalize(text)
    for term, data in lexicon.items():
        norm_term = normalize(term)
        # regex με boundaries για να μη βρίσκει "Νίκη" μέσα στη "Θεσσαλονίκη"
        pattern = r"\b" + re.escape(norm_term) + r"\b"
        if re.search(pattern, norm_text):
            terms_found.append((term, data["uri"]))
    return terms_found

# -----------------------
# Σύνδεση όρων με URIs
# -----------------------
def link_terms(text, terms_found):
    linked_text = text
    for term, uri in terms_found:
        # regex με boundaries, case-insensitive
        pattern = r"\b" + re.escape(term) + r"\b"
        linked_text = re.sub(pattern, f"[{term}]({uri})", linked_text, flags=re.IGNORECASE)
    return linked_text


def lex_semantics_geo(user_input):

    if user_input.strip():
        # Φόρτωσε πρώτα το lexicon
        try:
            with open("data/lexika/places_semantics.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            lexicon = jsonld_to_lexicon(data)
        except FileNotFoundError:
            st.error("We did not find it (semantics_places.json).")
            lexicon = {}

        # Τώρα κάλεσε την extract_terms με το lexicon
        terms_found = extract_terms(user_input, lexicon)
        linked_text = link_terms(user_input, terms_found)
        st.markdown(linked_text)
        st.markdown("#### I found these terms:")
        for term, uri in terms_found:
            st.markdown(f"- [{term}]({uri})")
    else:
        st.warning("Please enter text")

def prosthese_links(keimeno, lexiko):
    for lexi, link in lexiko.items():
        pattern = re.compile(rf"\b{re.escape(lexi)}\b", re.IGNORECASE)
        
        if isinstance(link, str) and link.startswith("http"):
            replacement = f"[{lexi}]({link})"
        else:
            replacement = f"<button class='popup-btn' onclick=\"window.dispatchEvent(new CustomEvent('showPopup', {{detail: '{lexi}'}}))\">{lexi}</button>"
        
        keimeno = pattern.sub(replacement, keimeno)
    return keimeno

lexiko_aplo = {
    "AI": "https://el.wikipedia.org/wiki/Τεχνητή_νοημοσύνη",
    "Python": "https://www.python.org/",
    "BERT": "https://en.wikipedia.org/wiki/BERT_(language_model)",
    "Knowledge Graph": "https://en.wikipedia.org/wiki/Knowledge_graph"
}

def lex_add_links_esoteriko(user_input):
    st.subheader("📘 Παραπομπές σε Λεξικό")

    if st.button("🔗 Μετατροπή σε κείμενο με links"):
        if user_input.strip():
            linked_text = prosthese_links(user_input, lexiko_aplo)
            st.markdown(linked_text, unsafe_allow_html=False)
        else:
            st.warning("Παρακαλώ γράψε ή επικόλλησε ένα κείμενο πρώτα.")


Path_test_lexiko = "data/lexika/test_lexiko.json"
Path_taxhorizon = "data/lexika/taxhorizon.json"

with open(Path_test_lexiko, "r", encoding="utf-8") as f:
    lexiko_exoteriko = json.load(f)

def lex_add_links_exoteriko(user_input):
    
    if user_input.strip():
        linked_text = prosthese_links(user_input, lexiko_exoteriko)
        st.markdown(linked_text, unsafe_allow_html=True)
    else:
        st.warning("First enter your text")



##### Οικονομικό λεξικό 

with open(Path_taxhorizon, "r", encoding="utf-8") as f:
    lexiko_list = json.load(f)

# Μετατροπή της λίστας σε λεξικό
lexiko_oikonomiko = {entry["list-s1"]: entry["list-s1 href"] for entry in lexiko_list}
lexiko_normalized = {
    normalize_greek(key): value
    for key, value in lexiko_oikonomiko.items()
}

def lex_oikonomikon(user_input):
    user_input = normalize_greek(user_input)
    if user_input.strip():
        linked_text = prosthese_links(user_input, lexiko_normalized)
        st.markdown(linked_text, unsafe_allow_html=True)
    else:
        st.warning("Please input text first")



user_input = st.text_area("enter text")
if st.button("Βάλε λινκ"):
    lex_oikonomikon(user_input)