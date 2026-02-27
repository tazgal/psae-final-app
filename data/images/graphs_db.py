
'''
Θέλω να φτιάξεις για python τα εξής:
1. μια ΒΔ με το όνομα graphs_db, και έναν πίνακα για αρχή που να περιέχει τις εξής στήλες: 
α. όνομα_γραφήματος (υποχρεωτικό), ημερομηνία_καταχώρησης (date), περιγραφή (text), ετικέτες (πολλαπλές επιλογές), πηγή, διεύθυνση
2. μια def που να "διαβάζει" από συγκεκριμένο φάκελο αρχεία με κατάληξη .png, .jpg, .pdf 
και αν δεν υπάρχουν ήδη στη ΒΔ να καταχωρεί (ρωτώντας με) τις παραπάνω τιμές. 
Δε θέλω να με ρωτάει για: ημερομηνία καταχώρησης (θέλω να είναι αυτόματη ανάλογα με την ημερομηνία που περνάει το αρχείο)
και διεύθυνση (θέλω να είναι απλά το path της εικόνας για να υπάρχει πρόσβαση)
3. μια def με την οποία να μπορώ να κάνω αναζήτηση ανά όνομα γραφήματος, περιγραφή κοκ και να μου ανοίγει το ανάλογο γράφημα
'''

import sqlite3
from pathlib import Path
from datetime import datetime
import os
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

DB_NAME = "graphs_db.sqlite"

def init_db():
    """Δημιουργεί τη ΒΔ και τον πίνακα αν δεν υπάρχουν."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS graphs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            όνομα_γραφήματος TEXT NOT NULL,
            ημερομηνία_καταχώρησης DATE DEFAULT CURRENT_DATE,
            περιγραφή TEXT,
            ετικέτες TEXT,
            πηγή TEXT,
            διεύθυνση TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_new_graphs_from_folder(folder_path):
    """Σαρώνει φάκελο για .png, .jpg, .pdf και καταχωρεί νέα αρχεία."""
    folder = Path(folder_path)
    if not folder.exists():
        print("Ο φάκελος δεν υπάρχει.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for file in folder.glob("*"):
        if file.suffix.lower() in [".png", ".jpg", ".pdf"]:
            # Έλεγχος αν υπάρχει ήδη
            c.execute("SELECT COUNT(*) FROM graphs WHERE διεύθυνση=?", (str(file),))
            if c.fetchone()[0] == 0:
                print(f"\nΒρέθηκε νέο αρχείο: {file.name}")
                name = input("Όνομα γραφήματος: ")
                desc = input("Περιγραφή: ")
                tags = input("Ετικέτες (χωρισμένες με κόμμα): ")
                source = input("Πηγή: ")

                c.execute("""
                    INSERT INTO graphs (όνομα_γραφήματος, περιγραφή, ετικέτες, πηγή, διεύθυνση)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, desc, tags, source, str(file)))
                conn.commit()
            else:
                print(f"Ήδη καταχωρημένο: {file.name}")

    conn.close()

def search_and_open(keyword):
    """Αναζητά γραφήματα ανά λέξη-κλειδί και ανοίγει το επιλεγμένο."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = """
        SELECT id, όνομα_γραφήματος, περιγραφή, ετικέτες, πηγή, διεύθυνση
        FROM graphs
        WHERE όνομα_γραφήματος LIKE ?
           OR περιγραφή LIKE ?
           OR ετικέτες LIKE ?
           OR πηγή LIKE ?
    """
    like_kw = f"%{keyword}%"
    c.execute(query, (like_kw, like_kw, like_kw, like_kw))
    rows = c.fetchall()

    if not rows:
        print("Δεν βρέθηκαν αποτελέσματα.")
    else:
        print("\nΑποτελέσματα:")
        for r in rows:
            print(f"{r[0]}. {r[1]} | Ετικέτες: {r[3]} | Πηγή: {r[4]}")
        choice = input("Δώσε ID για άνοιγμα (ή Enter για έξοδο): ")
        if choice.strip():
            chosen = next((r for r in rows if str(r[0]) == choice.strip()), None)
            if chosen:
                path = chosen[5]
                if os.path.exists(path):
                    webbrowser.open(path)
                else:
                    print("Το αρχείο δεν βρέθηκε στο δίσκο.")
    conn.close()

def search_and_open_all(keyword):
    """Αναζητά γραφήματα και ανοίγει κατευθείαν όλα τα αποτελέσματα."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = """
        SELECT όνομα_γραφήματος, διεύθυνση
        FROM graphs
        WHERE όνομα_γραφήματος LIKE ?
           OR περιγραφή LIKE ?
           OR ετικέτες LIKE ?
           OR πηγή LIKE ?
    """
    like_kw = f"%{keyword}%"
    c.execute(query, (like_kw, like_kw, like_kw, like_kw))
    rows = c.fetchall()

    if not rows:
        print("Δεν βρέθηκαν αποτελέσματα.")
    else:
        print("\nΑνοίγω τα εξής γραφήματα:")
        for name, path in rows:
            print(f"- {name}")
            if os.path.exists(path):
                webbrowser.open(path)
            else:
                print(f"  ⚠ Το αρχείο δεν βρέθηκε: {path}")
    conn.close()

def search_and_open_all2():
    """Αναζητά γραφήματα και ανοίγει κατευθείαν όλα τα αποτελέσματα."""
    keyword = input("Παρακαλώ βάλτε τον όρο αναζήτησης ").strip()

    like_kw = f"%{keyword}%"
    query = """
        SELECT όνομα_γραφήματος, διεύθυνση
        FROM graphs
        WHERE όνομα_γραφήματος LIKE ?
           OR περιγραφή LIKE ?
           OR ετικέτες LIKE ?
           OR πηγή LIKE ?
    """

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(query, (like_kw, like_kw, like_kw, like_kw))
        rows = c.fetchall()

    if not rows:
        print("Δεν βρέθηκαν αποτελέσματα.")
        return

    print("\nΑνοίγω τα εξής γραφήματα:")
    for name, path in rows:
        print(f"- {name}")
        if os.path.exists(path):
            img = mpimg.imread(path)   # ✅ Χρήση του path
            plt.imshow(img)
            plt.axis('off')
            plt.title(name)
            plt.show()
        else:
            print(f"  ⚠ Το αρχείο δεν βρέθηκε: {path}")

def search_and_open_all3():
    """Αναζητά γραφήματα και ανοίγει κατευθείαν όλα τα αποτελέσματα, τυπώνοντας και την περιγραφή."""
    keyword = input("Παρακαλώ βάλτε τον όρο αναζήτησης ").strip()

    like_kw = f"%{keyword}%"
    query = """
        SELECT όνομα_γραφήματος, διεύθυνση, περιγραφή
        FROM graphs
        WHERE όνομα_γραφήματος LIKE ?
           OR περιγραφή LIKE ?
           OR ετικέτες LIKE ?
           OR πηγή LIKE ?
    """

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(query, (like_kw, like_kw, like_kw, like_kw))
        rows = c.fetchall()

    if not rows:
        print("Δεν βρέθηκαν αποτελέσματα.")
        return

    print("\nΑνοίγω τα εξής γραφήματα:")
    for name, path, desc in rows:            # ✅ παίρνουμε και την περιγραφή
        print(f"- {name}")
        print(f"  Περιγραφή: {desc}")         # ✅ τυπώνουμε την περιγραφή
        if os.path.exists(path):
            img = mpimg.imread(path)          # Χρήση του path
            plt.imshow(img)
            plt.axis('off')
            plt.title(name)
            plt.show()
        else:
            print(f"  ⚠ Το αρχείο δεν βρέθηκε: {path}")

#add_new_graphs_from_folder("/Users/tazgal/*CODE/Graphs_DB")
            
#search_and_open_all3()
