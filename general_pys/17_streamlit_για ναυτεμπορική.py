
from bs4 import BeautifulSoup
import requests
import streamlit as st

def πάρε_τίτλους(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h2", class_="item-title")

        τίτλοι = []
        for title in titles:
            τίτλοι.append(title.text.strip())
        return τίτλοι
    else:
        return []

st.title("Δοκιμή search σε Ναυτεμπορική")

url = st.text_input("Βάλε το URL της σελίδας για να πάρεις τίτλους:", "https://www.naftemporiki.gr/kosmos/")

keywords_input = st.text_input("Βάλε λέξεις κλειδιά χωρισμένες με κόμμα:")

if st.button("Αναζήτηση"):
    if url and keywords_input:
        keywords = [k.strip().lower() for k in keywords_input.split(",")]
        τίτλοι = πάρε_τίτλους(url)

        found = False
        for title in τίτλοι:
            title_lower = title.lower()
            if any(keyword in title_lower for keyword in keywords):
                st.write(title)
                found = True
        if not found:
            st.write("Δεν βρέθηκαν τίτλοι με τις λέξεις κλειδιά.")
    else:
        st.write("Παρακαλώ βάλε URL και λέξεις κλειδιά.")