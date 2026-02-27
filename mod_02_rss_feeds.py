import feedparser 
import streamlit as st
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import pandas as pd



def feed_read_902():
    url = "https://www.902.gr/feed/recent"
    feed = feedparser.parse(url)
    print("Title: ", feed.feed.title)
    for entry in feed.entries:
        print("Title:", entry.title)
        print("link", entry.link)
        if hasattr(entry,"published"):
            print("Published:", entry.published)
        print("----")

def feed_read_902_streamlit():
    url = "https://www.902.gr/feed/recent"
    feed = feedparser.parse(url)
    st.write("Title: ", feed.feed.title)
    for entry in feed.entries:
        st.write("Title:", entry.title)
        st.write("link", entry.link)
        if hasattr(entry,"published"):
            st.write("Published:", entry.published)
        st.write("----")

def feed_read_rizospastis_streamlit():
    url = "https://www.rizospastis.gr/rssFeed.do?channel=Top"
    feed = feedparser.parse(url)
    st.write("Title: ", feed.feed.title)
    for entry in feed.entries:
        st.write("Title:", entry.title)
        st.write("link", entry.link)
        if hasattr(entry,"published"):
            st.write("Published:", entry.published)
        st.write("----")


def feed_google_news_streamlit():
    st.subheader("Google News Economy Feed")

    feed_url = "https://news.google.com/rss/search?q=global+economy&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:10]:
        soup = BeautifulSoup(entry.summary, "html.parser")
        clean_summary = soup.get_text()

        st.markdown(f"#### [{entry.title}]({entry.link})")
        st.write(clean_summary)
        st.caption(entry.published)
        st.divider()

def feed_to_R_db():
    RSS_URL = "https://www.rizospastis.gr/rssFeed.do?channel=Top"

    conn = sqlite3.connect("DBs/news_rss_R3.db")
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT UNIQUE,
        published TEXT,
        text TEXT,
        summary TEXT,
        source TEXT
    )
    ''')

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", datetime.now().isoformat())
        text = entry.get("text", "")
        summary = entry.get("summary", "")
        source = feed.feed.get("title", "Άγνωστη Πηγή")

        try:
            c.execute(
                "INSERT INTO articles (title, link, published, text, summary, source) VALUES (?, ?, ?, ?, ?, ?)",
                (title, link, published, text, summary, source)
            )
            print(f"✅ Αποθηκεύτηκε: {title}")
        except sqlite3.IntegrityError:
            print(f"⏩ Ήδη υπάρχει: {title}")

    conn.commit()
    conn.close()


def show_R_DB_streamlit():
    conn = sqlite3.connect("DBs/news_rss_R3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles ORDER BY published DESC")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["id", "title", "link", "published", "text", "summary", "source"])
    
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "link": st.column_config.LinkColumn(
                label="Link",
            )
        }
        )
  

def show_R_DB_streamlit2():
    conn = sqlite3.connect("news_rss_R3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles ORDER BY published DESC")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["id", "title", "link", "published", "text", "summary", "source"])
    
     # Δημιουργία clickable link
    df["link"] = df["link"].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')


    # Εμφάνιση σε HTML table
    st.markdown(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )


def feed_rss_streamlit(url):
    feed = feedparser.parse(url)
    st.write("Title: ", feed.feed.title)
    for entry in feed.entries:
        st.write("Title:", entry.title)
        st.write("link", entry.link)
        if hasattr(entry,"published"):
            st.write("Published:", entry.published)
        st.write("----")

