# Δοκιμή για streamlit

import streamlit as st
from newspaper import Article
import nltk
import pandas as pd

if 'news_df' not in st.session_state:
    st.session_state.news_df = pd.DataFrame(columns=['Title', 'Date', 'Text', 'Summary', 'Keywords', 'url'])


def scrap(url):  
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    Τίτλος = article.title
    Ημερομηνία = article.publish_date
    Κείμενο = article.text
    Σύνοψη = article.summary
    Keywords = article.keywords

    st.header("Τίτλος")
    st.write(Τίτλος)

    st.header("Date")
    st.write(Ημερομηνία)

    st.header("Κείμενο")
    st.write(Κείμενο)

    st.header("Σύνοψη")
    st.write(Σύνοψη)

    st.header("Λέξεις κλειδιά")
    st.write(Keywords)



    # Επιστροφή όλων των δεδομένων ως λεξικό
    return {
        'Τίτλος': article.title,
        'Ημερομηνία': article.publish_date,
        'Κείμενο': article.text,
        'Σύνοψη': article.summary,
        'Keywords': article.keywords,
        'url': url  # Προσθήκη του URL στα δεδομένα
    }


def new_row(data, news_df):  # Δέχεται τα δεδομένα και το DataFrame ως ορίσματα
    new_row = {
        'Title': data['Τίτλος'],
        'Date': data['Ημερομηνία'],
        'Text': data['Κείμενο'],
        'Summary': data['Σύνοψη'],
        'Keywords': data['Keywords'],
        'url': data['url']
    }
    # Προσθήκη νέας σειράς με pd.concat (πιο αποδοτικό από το .loc)
    return pd.concat([news_df, pd.DataFrame([new_row])], ignore_index=True)

def main_image(url):
    article = Article(url)
    article.download()
    article.parse()
    st.image(article.top_image, caption="Κύρια φωτογραφία")

######## Από εδώ και κάτω #######


st.markdown("## Δοκιμή scraping ειδήσεων")
url = st.text_input("Σε ποιό url θες να κάνουμε scraping;")
st.write(f"Οπότε κάνουμε σκράπινγκ σε αυτό {url}")

click_scrap = st.button("Πάτα εδώ για scraping")
click_save = st.button("Πάτα εδώ για αποθήκευση σε df")
click_photo = st.button("Πάτα εδώ για να δεις τη βασική φωτό")

if click_scrap == True:
    scrap(url)


if click_save:
    data = scrap(url)  # Παίρνουμε τα δεδομένα
    st.session_state.news_df = new_row(data, st.session_state.news_df)
    st.write(st.session_state.news_df)  # Δείχνουμε τον πίνακα

if click_photo == True:
    main_image(url)