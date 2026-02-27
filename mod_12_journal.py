import streamlit as st
import sqlite3
from datetime import date

# --- Σύνδεση/Δημιουργία Βάσης Δεδομένων ---

def imerologio():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date DATE,
            title TEXT,
            description TEXT
        )
    ''')
    conn.commit()

    st.title("📅 Ημερολόγιο Tasks")

    # --- Φόρμα Καταχώρησης ---
    st.subheader("➕ Καταχώρησε νέο task")
    with st.form("new_task_form"):
        selected_date = st.date_input("Ημερομηνία", value=date.today())
        title = st.text_input("Τίτλος")
        description = st.text_area("Περιγραφή")
        submitted = st.form_submit_button("Αποθήκευση")

        if submitted:
            if title.strip():
                c.execute("INSERT INTO tasks (task_date, title, description) VALUES (?, ?, ?)",
                        (selected_date, title, description))
                conn.commit()
                st.success("✅ Το task αποθηκεύτηκε!")
            else:
                st.warning("Δώσε τουλάχιστον τίτλο.")

    st.write("--------")
    st.subheader("📌 Σημερινά tasks")

    today = date.today()

    c.execute("""
        SELECT task_date, title, description
        FROM tasks
        WHERE DATE(task_date) = DATE(?)
        ORDER BY id
    """, (today,))
    today_rows = c.fetchall()

    if today_rows:
        for r in today_rows:
            # Μετατροπή ISO string -> date
            task_dt = date.fromisoformat(r[0])
            st.markdown(f"**{task_dt.strftime('%d/%m/%Y')}** – **{r[1]}**: {r[2]}")
    else:
        st.info("Δεν υπάρχουν tasks για σήμερα.")

    st.write("--------")
    st.subheader("📋 Προγραμματισμένα tasks")
    view_date = st.date_input("Εμφάνιση tasks για:", value=date.today(), key="view")
    c.execute("SELECT id, title, description FROM tasks WHERE task_date = ?", (view_date,))
    rows = c.fetchall()

    if rows:
        for r in rows:
            st.markdown(f"**{r[1]}** – {r[2]}")
    else:
        st.info("Δεν υπάρχουν tasks για αυτή την ημερομηνία.")

    from datetime import timedelta

    st.write("--------")
    st.subheader("📅 This week")

    today = date.today()
    # Αρχή εβδομάδας: Δευτέρα
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    # SQLite αποθηκεύει το task_date ως TEXT (YYYY-MM-DD) αν το αφήσαμε έτσι.
    # Αν το κρατάς σε αυτή τη μορφή, το query είναι:
    c.execute("""
        SELECT task_date, title, description
        FROM tasks
        WHERE DATE(task_date) BETWEEN DATE(?) AND DATE(?)
        ORDER BY DATE(task_date)
    """, (monday, sunday))
    week_rows = c.fetchall()

    if week_rows:
        for r in week_rows:
            # r[0] = ημερομηνία σε ISO string (YYYY-MM-DD)
            task_dt = date.fromisoformat(r[0])
            st.markdown(f"**{task_dt.strftime('%d/%m/%Y')}** – **{r[1]}**: {r[2]}")
    else:
        st.info("Δεν υπάρχουν tasks για αυτή την εβδομάδα.")
