import streamlit as st
from newspaper import Article
import pandas as pd

# Δημιουργία κενού DataFrame αν δεν υπάρχει
if 'news_df' not in st.session_state:
    st.session_state.news_df = pd.DataFrame(columns=['Title', 'Date', 'Text', 'Summary', 'Keywords', 'url'])

if 'last_scrap' not in st.session_state:
    st.session_state.last_scrap = None

def scrap(url):  
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    data = {
        'Τίτλος': article.title,
        'Ημερομηνία': article.publish_date,
        'Κείμενο': article.text,
        'Σύνοψη': article.summary,
        'Keywords': article.keywords,
        'url': url
    }

    # Εμφάνιση
    st.header("Τίτλος")
    st.write(data['Τίτλος'])
    st.header("Date")
    st.write(data['Ημερομηνία'])
    st.header("Κείμενο")
    st.write(data['Κείμενο'])
    st.header("Σύνοψη")
    st.write(data['Σύνοψη'])
    st.header("Λέξεις κλειδιά")
    st.write(data['Keywords'])

    return data

def new_row(data, news_df):
    new_row = {
        'Title': data['Τίτλος'],
        'Date': data['Ημερομηνία'],
        'Text': data['Κείμενο'],
        'Summary': data['Σύνοψη'],
        'Keywords': data['Keywords'],
        'url': data['url']
    }
    return pd.concat([news_df, pd.DataFrame([new_row])], ignore_index=True)

########### UI ###########
st.markdown("## Δοκιμή scraping ειδήσεων")
url = st.text_input("Σε ποιό url θες να κάνουμε scraping;")

if st.button("Πάτα εδώ για scraping"):
    st.session_state.last_scrap = scrap(url)

if st.button("Πάτα εδώ για αποθήκευση"):
    if st.session_state.last_scrap:
        st.session_state.news_df = new_row(st.session_state.last_scrap, st.session_state.news_df)
        st.success("Αποθηκεύτηκε!")
    else:
        st.warning("Δεν έχει γίνει scraping ακόμα!")

# Προβολή DataFrame
st.dataframe(st.session_state.news_df)
