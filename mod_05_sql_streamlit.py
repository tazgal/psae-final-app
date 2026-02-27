import streamlit as st
import sqlite3
import pandas as pd


DB_NAME = "DBs/news_05.db"

def sq_db_connect():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor


def view_all():
    conn, cursor = sq_db_connect()
    cursor.execute("SELECT * FROM news_table ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
    
def search_titles(term):
    conn, cursor = sq_db_connect()
    cursor.execute("SELECT * FROM news_table WHERE title LIKE ? ORDER BY date DESC", (f"%{term}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_news(title, date, url, text, summary, keywords):
    conn, cursor = sq_db_connect()
    cursor.execute("INSERT INTO news_table (title, date, url, text, summary, keywords) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, date, url, text, summary, keywords))
    conn.commit()
    conn.close()


def update_news(news_id, column, new_value):
    conn, cursor = sq_db_connect()
    cursor.execute(f"UPDATE news_table SET {column} = ? WHERE id = ?", (new_value, news_id))
    conn.commit()
    conn.close()


def delete_news(news_id):
    conn, cursor = sq_db_connect()
    cursor.execute("DELETE FROM news_table WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()


# ---------------- STREAMLIT UI ----------------
def main_db_streamlit():
    st.title("Διαχείριση Βάσης Ειδήσεων")

    menu = ["Προβολή όλων", "Αναζήτηση", "Προσθήκη", "Ενημέρωση", "Διαγραφή"]
    choice = st.sidebar.selectbox("Μενού", menu)

    if choice == "Προβολή όλων":
        st.subheader("📋 Όλες οι Ειδήσεις")
        data = view_all()
        df = pd.DataFrame(data, columns=["id", "title", "date", "url", "text", "summary", "keywords"])
        st.dataframe(df, use_container_width=True)

    elif choice == "Αναζήτηση":
        st.subheader("🔍 Αναζήτηση")
        term = st.text_input("Δώσε λέξη-κλειδί")
        if st.button("Αναζήτηση"):
            results = search_titles(term)
            df = pd.DataFrame(results, columns=["id", "title", "date", "url", "text", "summary", "keywords"])
            st.dataframe(df, use_container_width=True)

    elif choice == "Προσθήκη":
        st.subheader("➕ Προσθήκη Ειδήσεων")
        title = st.text_input("Τίτλος")
        date = st.text_input("Ημερομηνία")
        url = st.text_input("URL")
        text = st.text_area("Κείμενο")
        summary = st.text_area("Σύνοψη")
        keywords = st.text_input("Λέξεις-κλειδιά")
        if st.button("Αποθήκευση"):
            insert_news(title, date, url, text, summary, keywords)
            st.success("✅ Η εγγραφή προστέθηκε!")

    elif choice == "Ενημέρωση":
        st.subheader("✏️ Ενημέρωση Εγγραφών")
        news_id = st.number_input("ID Ειδήσης", min_value=1, step=1)
        column = st.selectbox("Στήλη", ["title", "date", "url", "text", "summary", "keywords"])
        new_value = st.text_area("Νέα Τιμή")
        if st.button("Ενημέρωση"):
            update_news(news_id, column, new_value)
            st.success(f"✅ Ενημερώθηκε η στήλη {column} για το ID {news_id}")

    elif choice == "Διαγραφή":
        st.subheader("🗑️ Διαγραφή Εγγραφής")
        news_id = st.number_input("ID Ειδήσης για Διαγραφή", min_value=1, step=1)
        if st.button("Διαγραφή"):
            delete_news(news_id)
            st.success(f"❌ Η εγγραφή με ID {news_id} διαγράφηκε")
    if __name__ == "__main__":
        main()



