import sqlite3
import os
import streamlit as st
import pandas as pd
from pathlib import Path
from docx import Document 
import json



# --- Ρυθμίσεις ---
DB_NAME = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/agenda.db"
FOLDER = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/agenda"

# --- 1. Δημιουργία Βάσης & Πίνακα ---
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keimena TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Η βάση και ο πίνακας 'texts' είναι έτοιμα.")


# --- 2. Διαβάζει περιεχόμενο αρχείου ---
def open_text_sp(file):
    with open(f"{file}.txt", "r", encoding="utf-8") as f:
        return f.read()


# --- 3. Φορτώνει όλα τα .txt από τον φάκελο ---
def open_files_from_folder():
    os.chdir(FOLDER)
    files = []
    for file in os.listdir(FOLDER):
        if file.endswith(".txt"):
            filename_without_ext = os.path.splitext(file)[0]
            text = open_text_sp(filename_without_ext)
            files.append(text)
            print(f"📄 Found: {file}")
    return files


# --- 4. Προσθήκη κειμένου στη ΒΔ ---
def add_to_db(import_text):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # --- Έλεγχος αν υπάρχει ---
    cur.execute("SELECT 1 FROM texts WHERE keimena = ?", (import_text,))
    exists = cur.fetchone()

    if exists:
        print("⚠️ Το κείμενο υπάρχει ήδη – δεν αποθηκεύτηκε ξανά.")
    else:
        cur.execute("INSERT INTO texts (keimena) VALUES (?)", (import_text,))
        conn.commit()
        print("✅ Το κείμενο προστέθηκε.")

    conn.close()


# --- 5. Επιστροφή όλων των κειμένων από τη ΒΔ ---
def show_texts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    q = "SELECT id, keimena FROM texts"
    cursor.execute(q)
    rows = cursor.fetchall()
    conn.close()
    return rows


# --- 6. Κύρια συνάρτηση ---
def open_files_save_to_db():
    create_db()  # δημιουργεί πίνακα αν δεν υπάρχει
    texts = open_files_from_folder()
    for text in texts:
        add_to_db(text)
    results = show_texts()
    print("\n🗂️ Όλα τα κείμενα στη ΒΔ:")
    for r in results:
        print(f"\nID: {r[0]}\nΚείμενο:\n{r[1]}\n{'-'*40}")


def agenda_streamlit():
    create_db()  # δημιουργεί πίνακα αν δεν υπάρχει
    texts = open_files_from_folder()
    for text in texts:
        add_to_db(text)
    results = show_texts()
    print("\n🗂️ Όλα τα κείμενα στη ΒΔ:")
    for r in results:
        st.write(f"\nID: {r[0]}\nΚείμενο:\n{r[1]}\n{'-'*40}")



def show_last_agenda_stream():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    q = "SELECT * FROM texts WHERE id = (SELECT MAX(id) FROM texts);"
    cursor.execute(q)
    last_row = cursor.fetchone() 
    conn.close()

    if last_row:
        st.write("🆔 ID:", last_row[0])
        st.write("📄 Κείμενο:\n", last_row[1])
    else:
        st.write("⚠️ Δεν βρέθηκαν εγγραφές.")


def show_last_agenda_stream2():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    q = "SELECT * FROM texts WHERE id = (SELECT MAX(id) FROM texts);"
    cursor.execute(q)
    last_row = cursor.fetchone()
    conn.close()

    if last_row:
        text = f"🆔 ID: {last_row[0]}\n\n📄 Κείμενο:\n{last_row[1]}"
        return text
    else:
        return "⚠️ Δεν βρέθηκαν εγγραφές."



def search_agenda_date_streamlit(date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, keimena, date FROM texts WHERE date = ?", (date,))
    row = cursor.fetchone()

    conn.close()

    if row:
        st.write("📅 Ημερομηνία:", row[2])
        st.write("📄 Κείμενο:\n", row[1])
    else:
        st.write("⚠️ Δεν βρέθηκε εγγραφή για αυτή την ημερομηνία.")

def search_agenda_date_streamlit2(date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, keimena, date FROM texts WHERE date = ?",
        (date,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        text = f"📅 Ημερομηνία: {row[2]}\n\n📄 Κείμενο:\n{row[1]}"
        return text
    else:
        return "⚠️ Δεν βρέθηκε εγγραφή για αυτή την ημερομηνία."

#open_files_save_to_db()
    
#Εναλλακτική προσέγγιση με dataframe:


def read_agenda_file(file_path):
    if file_path.suffix.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.suffix.lower() == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")

    
def load_txt_agenda_folder():
    folder_path = Path("data/agenda")
    data = []

    for file in folder_path.iterdir():
        if file.suffix not in [".txt", ".docx"]:
            continue

        try:
            date = pd.to_datetime(file.stem, errors="raise").date()
            text = read_agenda_file(file)

            data.append({
                "date": date,
                "text": text,
                "filename": file.name,
                "filetype": file.suffix
            })

        except Exception as e:
            print(f"⚠️ Πρόβλημα στο αρχείο {file.name}: {e}")

    df = pd.DataFrame(data)

    if df.empty:
        print("⚠️ Κανένα έγκυρο agenda αρχείο δεν φορτώθηκε")
        return df

    return df.sort_values("date")



def json_to_sqlite_dynamic(json_file, db_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Επεξεργασία κάθε κλειδιού στο JSON
    for key, value in data.items():
        print(f"Επεξεργασία: {key} (τύπος: {type(value).__name__})")
        
        if isinstance(value, list) and len(value) > 0:
            # Λίστα από αντικείμενα
            table_name = key
            
            # Εύρεση όλων των πιθανών στηλών
            all_keys = set()
            for item in value:
                if isinstance(item, dict):
                    all_keys.update(item.keys())
            
            if all_keys:
                # Δημιουργία SQL για τον πίνακα
                columns_def = []
                for col in all_keys:
                    columns_def.append(f'"{col}" TEXT')
                
                create_sql = f'''
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join(columns_def)}
                )
                '''
                
                cursor.execute(f"DROP TABLE IF EXISTS \"{table_name}\"")
                cursor.execute(create_sql)
                
                # Εισαγωγή δεδομένων
                for item in value:
                    if isinstance(item, dict):
                        columns = []
                        values = []
                        for col in all_keys:
                            columns.append(f'"{col}"')
                            values.append(str(item.get(col, '')))
                        
                        insert_sql = f'''
                        INSERT INTO "{table_name}" ({', '.join(columns)})
                        VALUES ({', '.join(['?'] * len(values))})
                        '''
                        cursor.execute(insert_sql, values)
        
        elif isinstance(value, dict):
            # Ενιαίο αντικείμενο
            table_name = f"{key}_info"
            
            # Δημιουργία πίνακα
            columns = [f'"{k}" TEXT' for k in value.keys()]
            
            create_sql = f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {', '.join(columns)}
            )
            '''
            
            cursor.execute(f"DROP TABLE IF EXISTS \"{table_name}\"")
            cursor.execute(create_sql)
            
            # Εισαγωγή δεδομένων
            columns_list = [f'"{k}"' for k in value.keys()]
            values_list = [str(v) for v in value.values()]
            
            insert_sql = f'''
            INSERT INTO "{table_name}" ({', '.join(columns_list)})
            VALUES ({', '.join(['?'] * len(values_list))})
            '''
            cursor.execute(insert_sql, values_list)
    
    conn.commit()
    
    # Έλεγχος
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nΔημιουργήθηκαν {len(tables)} πίνακες:")
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM "{table[0]}"')
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} εγγραφές")
    
    conn.close()
    return True

# Χρήση
#json_to_sqlite_dynamic('DBs/tasos_oiko.json', 'DBs/companies.db')