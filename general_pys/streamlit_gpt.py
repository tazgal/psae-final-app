import streamlit as st
from newspaper import Article
import pandas as pd

def scrap(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    return {
        'Τίτλος': article.title,
        'Ημερομηνία': article.publish_date,
        'Κείμενο': article.text,
        'Σύνοψη': article.summary,
        'Keywords': article.keywords,
        'url': url
    }

def new_row(data, df):
    new_row = {
        'Title': data['Τίτλος'],
        'Date': data['Ημερομηνία'],
        'Text': data['Κείμενο'],
        'Summary': data['Σύνοψη'],
        'Keywords': data['Keywords'],
        'url': data['url']
    }
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

st.title("Δοκιμή scraping ειδήσεων")

url = st.text_input("Σε ποιο url θες να κάνουμε scraping;")

if 'News_df' not in st.session_state:
    st.session_state.News_df = pd.DataFrame(columns=['Title', 'Date', 'Text', 'Summary', 'Keywords', "url"])

if 'last_article' not in st.session_state:
    st.session_state.last_article = None

if st.button("Πάτα εδώ για scraping"):
    if url:
        data = scrap(url)
        st.session_state.last_article = data
        st.header("Τίτλος")
        st.write(data['Τίτλος'])
        st.header("Ημερομηνία")
        st.write(data['Ημερομηνία'])
        st.header("Κείμενο")
        st.write(data['Κείμενο'])
        st.header("Σύνοψη")
        st.write(data['Σύνοψη'])
        st.header("Λέξεις κλειδιά")
        st.write(data['Keywords'])
    else:
        st.error("Παρακαλώ βάλε ένα URL!")

if st.button("Πάτα εδώ για αποθήκευση σε DataFrame"):
    if st.session_state.last_article is not None:
        st.session_state.News_df = new_row(st.session_state.last_article, st.session_state.News_df)
        st.success("Το άρθρο αποθηκεύτηκε στο DataFrame!")
        st.dataframe(st.session_state.News_df)
    else:
        st.error("Πρέπει πρώτα να κάνεις scraping!")

