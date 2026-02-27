# ********************* ΒΙΒΛΙΟΘΗΚΕΣ *********************

import sqlite3
from mod_01_enter_open import urls_to_list
from mod_02_scrap import news_scrap_newspaper3k_full,scrap_news_return_links2
from tabulate import tabulate
import streamlit as st
from pathlib import Path


# ********************* ΒΟΗΘΗΤΙΚΑ *********************

# Οι πίνακες μου: news_table / news_persons_rel / persons_table / place_table / events_table / tags / news_tags
#
#
#
#


# ********************* DEFS *********************


# Σε ένα πίνακα κάνει unique συγκεκριμένες στήλες ώστε αν είναι ίδιες να τις κάνει ignore
def sq_columns_unique_constraint(db, table, columns):
    """
    Δημιουργεί UNIQUE constraint (μέσω index) σε ήδη υπάρχοντα πίνακα.
    
    db      -> όνομα βάσης (π.χ. 'news_05.db')
    table   -> όνομα πίνακα (π.χ. 'place_table')
    columns -> λίστα από στήλες (π.χ. ['name', 'coordinates'])
    """

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Φτιάχνουμε όνομα index με βάση το table + columns
    index_name = f"idx_{table}_{'_'.join(columns)}"

    # Φτιάχνουμε την εντολή SQL
    cols = ", ".join(columns)
    q = f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table} ({cols});"

    cursor.execute(q)
    conn.commit()
    conn.close()

    print(f"✅ UNIQUE constraint δημιουργήθηκε για ({cols}) στον πίνακα {table}.")

# Καθαρίζει τα διπλότυπα και εφαρμόζει στις στήλες το κριτήριο unique
def sq_add_unique_constraint_clean(db, table, columns):
    """
    Καθαρίζει διπλότυπα και δημιουργεί UNIQUE constraint σε ήδη υπάρχοντα πίνακα.
    
    db      -> όνομα βάσης (π.χ. 'news_05.db')
    table   -> όνομα πίνακα (π.χ. 'news_table')
    columns -> λίστα από στήλες (π.χ. ['url', 'title', 'text'])
    """

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Καθαρίζουμε διπλότυπα
    cols = ", ".join(columns)
    delete_q = f"""
    DELETE FROM {table}
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM {table}
        GROUP BY {cols}
    );
    """
    cursor.execute(delete_q)
    conn.commit()

    # Φτιάχνουμε όνομα index
    index_name = f"idx_{table}_{'_'.join(columns)}"
    
    # Δημιουργούμε το UNIQUE index
    q = f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table} ({cols});"
    cursor.execute(q)
    conn.commit()
    conn.close()

    print(f"✅ UNIQUE constraint δημιουργήθηκε για ({cols}) στον πίνακα {table}. "
          "Διπλότυπα αφαιρέθηκαν.")
    
# ============> ΔΗΜΙΟΥΡΓΙΑ - ΣΥΝΔΕΣΗ - INSPECT 
def sq_create_db():
    name = input("Enter db name to create ")
    conn = sqlite3.connect(f"{name}.db")
    print(f"DB {name} was created")
    conn.commit()
def sq_db_connect_or_create(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()
    print(f"✅ Συνδέθηκες στη βάση {db_name}.db")
    return conn, cursor
# βλέπεις τους πίνακες και τις εγγραφές που έχει μια ΒΔ
def sq_inspect_db(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    # 1. Βρες όλους τους πίνακες
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("Δεν βρέθηκαν πίνακες στη βάση.")
        return

    print(f"\n📂 Πίνακες στη βάση '{db_name}':")
    for (table,) in tables:
        print(f"\n--- Πίνακας: {table} ---")

        # 2. Δες τις στήλες (δομή πίνακα)
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        print("Στήλες:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        # 3. Δες τις τελευταίες 5 γραμμές με βάση rowid
        cursor.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 5;")
        rows = cursor.fetchall()
        if rows:
            print("Τελευταίες εγγραφές:")
            for row in rows:
                print(" ", row)
        else:
            print("  (Δεν υπάρχουν εγγραφές ακόμα)")

    conn.close()

# Δείχνει (δεν επιστρέφει) σειρές από τον πίνακα μας (συγκεκριμένης ΒΔ) είτε όλες είτε μιας στήλης
def sq_inspect_table_rows():
    db = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db)
    table = input("which table? options: news_table, persons_table, place_table, event_table, tags  ").strip()

    while True:
        search = input("press 1 to search all, 2 to for specific column, 3 to another table, 4 to stop ")

        if search == "1":
            cursor.execute(f"SELECT * FROM {table}")
            results = cursor.fetchall()
            
            for r in results:
                print(r)
        elif search == "2":
            col_name = input("enter column name ").strip()
            
            try:
                cursor.execute(f" SELECT {col_name} FROM {table}")
                results2 = cursor.fetchall()

                for r in results2:
                    print(r)

            except sqlite3.Error as e:
                print(f"σφάλμα {e}")
        
        elif search == "3":
            table = input("enter new table name ")
            print(f"switched to {table}")

        elif search == "4":
            break
        else:
            print("this is not an option")

# Το ίδιο, αλλά διαλέγω περισσότερες στήλες να μου δείξει
def sq_inspect_table_multirows():
    db = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db)
    table = input("which table? ")

    while True:
        search = input("press 1 to search all, 2 to for specific columns, 3 to another table, 4 to stop ")

        if search == "1":
            cursor.execute(f"SELECT * FROM {table}")
            results = cursor.fetchall()
            
            for r in results:
                print(r)
        elif search == "2":
            col_name1 = input("enter column 1 name here ").strip()
            col_name2 = input("enter col 2 name here ").strip()

            try:
                cursor.execute(f" SELECT {col_name1}, {col_name2} FROM {table}")
                results2 = cursor.fetchall()

                for r in results2:
                    print(r)

            except sqlite3.Error as e:
                print(f"σφάλμα {e}")
        
        elif search == "3":
            continue
        elif search == "4":
            break
        else:
            print("this is not an option")

# Συγκεντρώνει όλα τα inspect
def sql_super_inspect():
    db = "DBs/news_05"
    x = input("\n what do you want to do? \n press 1. for db inspect \n 2. to see table rows \n 3. to see multiple columns ").strip()

    if x == "1":
        sq_inspect_db(db)
    elif x == "2":
        sq_inspect_table_rows()
    elif x == "3":
        sq_inspect_table_multirows()
    else:
        print("this is not an option")


# Διαλέγω στήλη από πίνακα - επιστρέφω τιμή που μπορεί να γίνει στήλη 
def sq_choose_column_from_table():
    db = input("enter db ")
    table = input("enter table ")
    column = input("enter column ")


    conn, cursor = sq_db_connect_or_create(db)
    query = f"SELECT {column} FROM {table}"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

    conn.commit()
    conn.close()
    return results
#Διαλέγω τη στήλη text από τον πίνακα news_table
def sq_choose_txt_column_from_newstable():

    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    query = "SELECT text FROM news_table"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

    conn.commit()
    conn.close()
    return results
# Το ίδιο αλλά απλά την επιστρέφει χωρίς να την τυπώνει
def sq_choose_txt_column_from_newstable_wtho_print():

    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    query = "SELECT text FROM news_table"
    cursor.execute(query)
    results = cursor.fetchall()
    
    conn.commit()
    conn.close()
    return results

def sq_choose_txt_column_spec_lines():

    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    query = "SELECT text FROM news_table"
    cursor.execute(query)
    results = cursor.fetchall()

    first_two = results[:4]

    conn.commit()
    conn.close()
    return first_two

# ============> ΠΡΟΣΘΗΚΗ ΠΙΝΑΚΩΝ ΤΙΜΩΝ ΚΟΚ 

def sql_super_add():
    conn = sqlite3.connect("DBs/news_05.db")
    cursor = conn.cursor

    selection = input('''Επιλέξτε τι θέλετε να κάνετε: \n
        1. για δημιουργία ΒΔ \n
        2. για δημιουργία πίνακα ή στήλης \n
        3. χειροκίνητη προσθήκη σε newstable \n
        4. προσθέτει πρόσωπο (όνομα, ιδιότητα, ολόκληρο όνομα) σε πρόσωπα \n
        5. Προσθέτει μέρος (της μορφής λατ, λον, όνομα) στον πίνακα places
                      
                      ''')
    
    if selection == "1":
        sq_create_db()
    elif selection == "2":
        sq_add_table_or_columns2()
    elif selection == "3":
        sq_add_values_to_news_table()
    elif selection == "4":
        sq_add_person_in_persons_table()
    elif selection == "5":
        sq_add_place_to_place_table()
    else:
        print("this is not an option")
    
        



# Προσθέτει σε μια συγκεκριμένη βάση τον συγκεκριμένο πίνακα "news" (που απλά του δίνεις ό,τι όνομα θες)
def sq_create_newstable_to_this_db(db_name, table_name):

    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()


    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Date TEXT,
            Url TEXT UNIQUE,
            Text TEXT,
            Summary TEXT,
            Keywords TEXT
        )
    """)

    print(f"table {table_name} created in {db_name} database")

    conn.commit()

# Παίρνει το όνομα της ΒΔ και δημιουργεί μέσα τον πίνακα που του ζητάς ή προσθέτεις στήλες
def sq_add_table_or_columns(db_name, table_name):

    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)")

    while True:
        print("για να προσθέσετε στήλη πατήστε 1, για τέλος πατήστε 2: ")
        x = input()
        

        if x == "1":
            print("εισάγετε το όνομα της στήλης: ")
            y = input()

            cursor.execute(f"""
                ALTER TABLE {table_name} ADD COLUMN {y} TEXT;
            """)
            conn.commit()
            print(f"Η στήλη {y} προστέθηκε στον πίνακα {table_name}")
        elif x == "2":
            break
        else:
            print("this is not an option")

    print(f"table {table_name} created in {db_name} database")

    conn.commit()
    conn.close()

# Το ίδιο αλλά ορίζεις το όνομα του πίνακα και τη ΒΔ μέσα
def sq_add_table_or_columns2():
    db_name = "DBs/news_05"
    table_name = input("Διαλέξτε το όνομα του πίνακα όπου θέλετε να προσθέσετε στήλη ")

    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)")

    while True:
        print("για να προσθέσετε στήλη πατήστε 1, για τέλος πατήστε 2: ")
        x = input()
        

        if x == "1":
            print("εισάγετε το όνομα της στήλης: ")
            y = input()

            cursor.execute(f"""
                ALTER TABLE {table_name} ADD COLUMN {y} TEXT;
            """)
            conn.commit()
            print(f"Η στήλη {y} προστέθηκε στον πίνακα {table_name}")
        elif x == "2":
            break
        else:
            print("this is not an option")

    print(f"table {table_name} created in {db_name} database")

    conn.commit()
    conn.close()

# Το ίδιο, αλλά προσθέτει με τη μια όλες τις στήλες ως λίστα  
def sq_add_list_as_columns(db_name,table_name,list_name):
    
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)")

    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_cols = [col[1] for col in cursor.fetchall()]

    # Προσθήκη στηλών μόνο αν δεν υπάρχουν
    for timi in list_name:
        if timi not in existing_cols:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {timi} TEXT;")
            print(f"✅ Η στήλη '{timi}' προστέθηκε στον πίνακα {table_name}.")
        else:
            print(f"⚠️ Η στήλη '{timi}' υπάρχει ήδη, την αγνόησα.")
        conn.commit()

    conn.commit()
    conn.close()


def sq_add_list_as_columns2():
    db_name = "DBs/news_05"
    table_name = input("Πρόσθεσε όνομα πίνακα ")
    list_name = input("Το όνομα της λίστας που έχει τις νέες στήλες ")

    
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)")

    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_cols = [col[1] for col in cursor.fetchall()]

    # Προσθήκη στηλών μόνο αν δεν υπάρχουν
    for timi in list_name:
        if timi not in existing_cols:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {timi} TEXT;")
            print(f"✅ Η στήλη '{timi}' προστέθηκε στον πίνακα {table_name}.")
        else:
            print(f"⚠️ Η στήλη '{timi}' υπάρχει ήδη, την αγνόησα.")
        conn.commit()

    conn.commit()
    conn.close()

# Προσθέτει συγκεκριμένη γραμμή στον πίνακα news (με τις 6 τιμές που έχει αυτός)
def sq_add_line_to_news(table_name):

    conn = sqlite3.connect(f"{table_name}.db")
    cursor = conn.cursor()

    title = input("pls enter title"),
    date = input("pls enter date"),
    url = input("pls enter url")
    text = input("pls enter text")
    summary = input("pls enter summary")
    keywords = input("pls enter keys")

    cursor.execute("""
        INSERT INTO news (Title, Date, Url, Text, Summary, Keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"{title}",
        f"{date}",
        f"{url}",
        f"{text}",
        f"{summary}",
        f"{keywords}"
        
    ))

    conn.commit()

# προσθέτει γραμμή νέων σε ΒΔ (προσοχή την έχω φιξ στην 5) με συνεχή input
def sq_add_values_to_news_table():
    db_name = "DBs/news_05"

    conn, cursor = sq_db_connect_or_create(db_name)

    x1 = input("please enter title")
    x2 = input("please enter date")
    x3 = input("please enter url")
    x4 = input("please enter text")
    x5 = input("please enter summary")
    x6 = input("please enter keywords")

    cursor.execute('INSERT into news_table (title, date, url, "text", summary, keywords) VALUES (?,?,?,?,?,?)', 
                (x1, x2, x3, x4, x5, x6))
    print("προστέθηκε η είδηση")
    conn.commit()
    conn.close()

# προσθέτει γραμμή νέων - που δίνονται ως λίστα - σε ΒΔ (προσοχή την έχω φιξ στην 5)
def sq_add_line_to_news_table(line):
    db_name = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db_name)

    cursor.execute(
        'INSERT OR IGNORE INTO news_table (title, date, url, "text", summary, keywords) '
        'VALUES (:title, :date, :url, :text, :summary, :keywords)',
        line  # dictionary εδώ
    )

    print("προστέθηκε η είδηση")
    conn.commit()
    conn.close()

# προσθέτει πρόσωπο σε πίνακα προσώπων
def sq_add_person_in_persons_table():

    db = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db)

    p_name = input("enter person name ")
    ident = input("enter ident ")
    full_name = input("enter full name") or None

    cursor.execute("INSERT OR IGNORE INTO persons_table (persons_name, identity, full_name) VALUES (?, ?, ?)",
                (p_name, ident,full_name) 
                
                )
    print(f"person {p_name} added to persons table")

    conn.commit()
    conn.close()

# προσθέτει λίστα προσώπων σε πρόσωπα 
def sq_add_persons_list_in_persons_table(persons_list):

    db = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db)

    for p_name, ident, full_name in persons_list:
        cursor.execute("INSERT OR IGNORE INTO persons_table (persons_name, identity, full_name) VALUES (?, ?, ?)",
                    (p_name, ident,full_name) 
                    
                    )
        print(f"person {p_name} added to persons table")

    conn.commit()
    conn.close()

# Προσθέτει μια λίστα με μέρη (της μορφής λατ, λον, όνομα) στον πίνακα places
def sq_add_list_to_place_table(db, list):
    
    conn, cursor = sq_db_connect_or_create(db)

    query = '''
    INSERT OR IGNORE INTO place_table (name, coordinates) VALUES (?, ?) ; 
    '''

    for lat, long, name in list:
        coordinates = f"({lat}, {long})"
        cursor.execute(query, (name, coordinates))
        print(f"{name} προστέθηκε")
    
    conn.commit()
    conn.close()





# =============> ΔΙΑΓΡΑΦΗ 
#Διαγραφή γραμμής 

    def sq_delete_row(db_name, table, row_id):
        conn = sqlite3.connect(db_name + ".db")
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
        
        conn.commit()
        conn.close()
        print(f"Η γραμμή με id={row_id} διαγράφηκε από τον πίνακα {table}")

def sq_add_place_to_place_table():

    conn = sqlite3.connect("DBs/news_05.db")
    cursor = conn.cursor()
    
    query = '''
    INSERT OR IGNORE INTO place_table (name, coordinates) VALUES (?, ?) ; 
    '''

    name = input("pls enter place name ")
    lat = input("pls enter latitude")
    long = input("pls enter longtitude")
    coordinates = f"({lat}, {long})"
    
    cursor.execute(query, (name, coordinates))
    print(f"{name} προστέθηκε")
    
    conn.commit()
    conn.close()


# Διαγραφή πίνακα 
def sq_delete_table(db_name,table_name):
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE {table_name}")
    print(f"--- Από την {db_name} Διαγράφηκε ο πίνακας {table_name} ---")
    conn.commit()
    conn.close()

# για διαγραφή στήλης από ένα πίνακα (τρελό ότι δεν υπάρχει απευθείας!)
def sq_drop_column(db_name, table_name, column_to_drop):
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

    # Παίρνουμε πληροφορίες για τις στήλες
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()
    all_columns = [col[1] for col in columns_info]

    if column_to_drop not in all_columns:
        print(f"Η στήλη '{column_to_drop}' δεν υπάρχει στον πίνακα '{table_name}'")
        conn.close()
        return

    # Κρατάμε μόνο τις στήλες που δεν θα διαγραφούν
    new_columns = [col for col in columns_info if col[1] != column_to_drop]

    # Χτίζουμε το CREATE TABLE με τους τύπους/constraints
    col_defs = []
    for col in new_columns:
        cid, name, ctype, notnull, dflt_value, pk = col
        col_def = f"{name} {ctype}" if ctype else f"{name}"
        if pk: col_def += " PRIMARY KEY"
        if notnull: col_def += " NOT NULL"
        if dflt_value is not None: col_def += f" DEFAULT {dflt_value}"
        col_defs.append(col_def)

    col_defs_str = ", ".join(col_defs)

    # 1. Δημιουργία νέου πίνακα με τις στήλες που μένουν
    cursor.execute(f"CREATE TABLE {table_name}_new ({col_defs_str});")

    # 2. Αντιγραφή δεδομένων
    cols_to_copy = ", ".join([c[1] for c in new_columns])
    cursor.execute(f"INSERT INTO {table_name}_new ({cols_to_copy}) SELECT {cols_to_copy} FROM {table_name};")

    # 3. Σβήνουμε τον παλιό πίνακα
    cursor.execute(f"DROP TABLE {table_name};")

    # 4. Μετονομάζουμε τον νέο πίνακα
    cursor.execute(f"ALTER TABLE {table_name}_new RENAME TO {table_name};")

    conn.commit()
    conn.close()
    print(f"Η στήλη '{column_to_drop}' διαγράφηκε από τον πίνακα '{table_name}'.")





# =============> ΑΝΑΖΗΤΗΣΗ 
# Ψάχνει με λέξη - κλειδί στους τίτλους της ΒΔ
def sq_search_to_titles():
    term = input("pls enter keyword ").strip()
    title_list = []
    db_name = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db_name)

    cursor.execute("SELECT title FROM news_table WHERE title LIKE ? ORDER BY date DESC", (f"%{term}%",))
    rows = cursor.fetchall()

    for row in rows:
        title_list.append(row[0])

    count = 0

    for item in title_list:
        print(item)
        count = count + 1

    print(f"Σύνολο ειδήσεων {count}")

    conn.close()
    return title_list

def sq_search_to_titles_streamlit():
    term = input("pls enter keyword ").strip()
    title_list = []
    db_name = "DBs/news_05"
    conn, cursor = sq_db_connect_or_create(db_name)

    cursor.execute("SELECT title FROM news_table WHERE title LIKE ? ORDER BY date DESC", (f"%{term}%",))
    rows = cursor.fetchall()

    for row in rows:
        title_list.append(row[0])

    count = 0

    for item in title_list:
        print(item)
        count = count + 1

    print(f"Σύνολο ειδήσεων {count}")

    conn.close()
    return title_list


def sq_search_to_titles_streamlit():
    term = st.text_input("Βάλε λέξη-κλειδί για αναζήτηση").strip()
    title_list = []
    db_name = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/DBs/news_05.db"
    conn, cursor = sq_db_connect_or_create(db_name)

    cursor.execute("SELECT title FROM news_table WHERE title LIKE ? ORDER BY date DESC", (f"%{term}%",))
    rows = cursor.fetchall()

    for row in rows:
        title_list.append(row[0])

    count = 0

    for item in title_list:
        st.write(item)
        count = count + 1

    st.write(f"Σύνολο ειδήσεων {count}")

    conn.close()
    return title_list

def sq_search_to_titles_streamlit2():
    term = st.text_input("Βάλε λέξη-κλειδί για αναζήτηση").strip()
    title_list = []

    DB_PATH = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/news_05.db")
    if not DB_PATH.exists():
        st.error(f"Η βάση δεν βρέθηκε: {DB_PATH}")
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT title FROM news_table WHERE title LIKE ? ORDER BY date DESC", (f"%{term}%",))
    rows = cursor.fetchall()

    for row in rows:
        title_list.append(row[0])
        st.write(row[0])

    st.write(f"Σύνολο ειδήσεων {len(title_list)}")
    conn.close()
    return title_list


# Εμφανίζει ημερομηνίες και τίτλους 
def sq_show_titles_dates():
    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    print("\n")
    print("---------- Σου εμφανίζω τίτλους και ημερομηνίες από τη ΒΔ news_05 ----------")
    print("\n")
    cursor.execute("SELECT title, date FROM news_table ORDER BY date DESC")
    rows = cursor.fetchall()

    for row in rows:
        title, date = row
        print(f"{title} // Ημερομηνία: {date}")
        print("-" * 30)

# Εμφανίζει τα url αυτών των τίτλων της ΒΔ
def sq_show_titles_urls():
    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    cursor.execute("SELECT title, url FROM news_table")
    rows = cursor.fetchall()

    for row in rows:
        title, url = row
        print(f"{title} ====> {url}")
    
    conn.close()

def sq_search_titles_urls():
    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    cursor.execute("SELECT title, url FROM news_table")
    rows = cursor.fetchall()
    keyword = input("enter keyword ").strip()


    found = False
    for title,url in rows:
        if keyword in title.lower():
            print(f"{title} ====> {url}")
            found = True
    
    if not found:
        print("keyword not found")

    conn.close()

# Ψάχνει στη ΒΔ τίτλους με λέξη κλειδί και επιστρέφει τα url τους
def sq_search_titles_and_get_urls():
    """
    Αναζητά τίτλους που περιέχουν το keyword και επιστρέφει τα URL τους.
    """
    conn = sqlite3.connect("DBs/news_05.db")
    cursor = conn.cursor()

    keyword = input("Βάλε λέξη-κλειδί: ").strip()

    # Χρησιμοποιούμε placeholder για ασφάλεια από SQL injection
    query = "SELECT title, url FROM news_table WHERE title LIKE ? ORDER BY date DESC ;"
    cursor.execute(query, (f"%{keyword}%",))  # % για "περιέχει"

    results = cursor.fetchall()  # επιστρέφει λίστα από tuples (title, url)
    for title, url in results:
        print(title)
        print(f"\033]8;;{url}\033\\{url}\033]8;;\033\\")
        print("\n")

    conn.close()

    # Φτιάχνουμε λεξικό ή λίστα για ευκολότερη χρήση
    output = [{"title": title, "url": url} for title, url in results]
    return output

# * Ψάχνει με λέξη κλειδί σε τίτλους και γυρνάει τίτλο, id, κείμενο κτλ όπως και αριθμό κειμένων 
def sq_search_titles_print_sth():
    conn, cursor = sq_db_connect_or_create("DBs/news_05")
    keyword1 = input("pls enter keyword ")
    keyword = f"%{keyword1}%"
    query = ("SELECT id, url, title, text FROM news_table WHERE title LIKE ?")
    cursor.execute(query, (keyword,))   
    results = cursor.fetchall()

    count = 0

    for row in results:
        print("----------------")
        print("Id:", row[0])
        print("Url:", row[1])
        print("Title:", row[2])
        print("Text \n", row[3])
        print("\n")
        print("----------------")
        count = count+1
    
    print(f"υπάρχουν {count} ειδήσεις")

    conn.close()

# Ψάχνει σε κείμενα των ειδήσεων
def sq_search_texts_print():
    conn = sqlite3.connect("DBs/news_05.db")
    cursor = conn.cursor()

    k1 = input("pls enter search word ")
    k2 = f"%{k1}%"

    query = "SELECT id, url, title, text FROM news_table WHERE text LIKE ? "
    cursor.execute(query, (k2, ))
    results = cursor.fetchall()

    count = 0

    for r in results:
        print("********")
        print("\n")
        print("id: ", r[0])
        print("\n")
        print("url: ", r[1])
        print("\n")
        print("title: ", r[2])
        print("\n")
        print("text: ", r[3])
        print("----------------------")
        count = count + 1

    print(f"Σύνολο ειδήσεων {count}")
    conn.close()

def sq_search_and_return_texts():
    conn, cursor = sq_db_connect_or_create("DBs/news_05")

    k1 = input("pls enter search word ")
    k2 = f"%{k1}%"

    query = "SELECT text FROM news_table WHERE text LIKE ? "
    cursor.execute(query, (k2, ))
    results = cursor.fetchall()

    for r in results:
        return r[0]
    
    conn.close()

# Ψάχνει ένα πρόσωπο που περιλαμβάνεται μέσα σε ειδήσεις - επιστρέφει ειδήσεις, τίτλους κτλ με ταξινόμηση στη στήλη ημερομηνίας
def sql_search_this_person():
    db = "DBs/news_05.db"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    person_name = input("enter persons name to search ").strip()

    q = """
        SELECT n.id, n.title, n.text, n.date
        FROM news_table n
        JOIN news_persons_rel r ON n.id = r.news_id
        JOIN persons_table p ON r.person_id = p.id
        WHERE p.persons_name = ?
        ORDER BY n.date ASC ;
    """

    cursor.execute(q, (person_name,))

    results = cursor.fetchall()
    for news_id, title, text, date in results:
        print(f"---- {title} -----")
        print("\n")
        print(f"{date}")
        print("\n")
        print(f"{text}")
        print("\n") 
        print("*********")
        print("\n") 

    conn.close()

# Ψάχνει δύο πρόσωπα που βρίσκονται στην ίδια είδηση 
def sql_search_two_persons():
    db = "DBs/news_05.db"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    person1 = input("enter first persons name to search ").strip()
    person2 = input("enter second persons name to search ").strip()

    q = '''
    SELECT n.id, n.title, n.text, n.date
    FROM news_table n
    JOIN news_persons_rel r1 ON n.id = r1.news_id
    JOIN persons_table p1 ON r1.person_id = p1.id
    JOIN news_persons_rel r2 ON n.id = r2.news_id
    JOIN persons_table p2 ON r2.person_id = p2.id
    WHERE p1.persons_name = ?
      AND p2.persons_name = ?
    ORDER BY n.date ASC ;
    '''

    cursor.execute(q, (person1, person2))
    results = cursor.fetchall()

    for news_id, title, text, date in results:
        print(f"---- {title} -----")
        print("\n")
        print(f"{date}")
        print("\n")
        print(f"{text}")
        print("\n") 
        print("*********")
        print("\n") 


    conn.close()

# Ψάχνει ειδήσεις με βάση τα tags στον σχετικό πίνακα
def sql_search_with_tags():

    keyword = input("Με βάση ποιό tag θα γυρίσω ειδήσεις;")

    q = f'''
        SELECT n.title, n.date 
        FROM news_table n
        JOIN news_tags nt ON n.id = nt.news_id
        JOIN tags t ON nt.tag_id = t.id
        WHERE t.name = {keyword};
    '''

    conn, cursor = sq_db_connect_or_create(db)
    cursor.execute(q)
    results = cursor.fetchall()


    print("--------------------------------------")
    print("αποτελέσματα για αναζήτηση με πολιτική")
    for x in results:
        print(x)
        print("\n")

    conn.close()

# Ψάχνει ειδήσεις με βάση τα ονόματα στον πίνακα των ονομάτων 
def sql_search_news_by_tablename():
    
    pers = input("Pls enter name to search ").strip()
    
    query = f'''
    SELECT n.title, n.date, n.url 
    FROM news_table n
    JOIN news_persons_rel np ON np.news_id = n.id
    JOIN persons_table p ON np.person_id = p.id
    WHERE p.persons_name = ?
    ORDER BY n.date ASC
    '''

    conn, cursor = sq_db_connect_or_create(db)
    cursor.execute(query, (pers, ))
    results = cursor.fetchall()

    for r in results:
        print(r[0])
        print(r[1])
        print(r[2])
        print("***")

    conn.commit()
    conn.close()

def sql_search_news_by_tablename_date():
    
    pers = input("Pls enter name to search: ").strip()
    start_date = input("Pls enter start date YYYY-MM-DD: ")
    end_date = input("Pls enter end date YYYY-MM-DD: ")
    
    
    query = '''
    SELECT n.title, n.date, n.url 
    FROM news_table n
    JOIN news_persons_rel np ON np.news_id = n.id
    JOIN persons_table p ON np.person_id = p.id
    WHERE p.persons_name = ?
    AND DATE(n.date) BETWEEN DATE(?) AND DATE(?)   
    ORDER BY n.date ASC
    '''

    conn, cursor = sq_db_connect_or_create(db)
    cursor.execute(query, (pers, start_date, end_date, ))
    results = cursor.fetchall()

    for r in results:
        print(r[0])
        print(r[1])
        print(r[2])
        print("***")

    conn.commit()
    conn.close()

def sql_super_search():
    x = input('''
Select what to search \n
    01. Ψάξε σε τίτλους \n
    02. Ψάξε σε τίτλους και πάρε τα url \n
    03. Ψάξε σε τίτλους και πάρε τίτλο, id, κείμενο κτλ όπως και αριθμό κειμένων  \n
    04. Ψάξε στα κείμενα των ειδήσεων \n
    05. Ψάξε ένα πρόσωπο μέσα σε ειδήσεις \n
    06. Ψάξε δύο πρόσωπα μέσα στην ίδια είδηση \n
    07. Ψάξε με tags \n
    08. Ψάξε με όνομα και ημερομηνίες \n
    
              ''')


    if x == "01":
        sq_search_to_titles()
    elif x == "02":
        sq_search_titles_and_get_urls()
    elif x == "03":
        sq_search_titles_print_sth()
    elif x == "04":
        sq_search_texts_print()
    elif x == "05":
        sql_search_this_person()
    elif x == "06":
        sql_search_two_persons()
    elif x == "07":
        sql_search_with_tags()
    elif x == "08":
        sql_search_news_by_tablename_date()
    else:
        print("this is not an option")



def sql_super_search_streamlit():
    x = st.text_input('''
Select what to search \n
    01. Ψάξε σε τίτλους \n
    02. Ψάξε σε τίτλους και πάρε τα url \n
    03. Ψάξε σε τίτλους και πάρε τίτλο, id, κείμενο κτλ όπως και αριθμό κειμένων  \n
    04. Ψάξε στα κείμενα των ειδήσεων \n
    05. Ψάξε ένα πρόσωπο μέσα σε ειδήσεις \n
    06. Ψάξε δύο πρόσωπα μέσα στην ίδια είδηση \n
    07. Ψάξε με tags \n
    08. Ψάξε με όνομα και ημερομηνίες \n
    
              ''')


    if x == "01":
        sq_search_to_titles()
    elif x == "02":
        sq_search_titles_and_get_urls()
    elif x == "03":
        sq_search_titles_print_sth()
    elif x == "04":
        sq_search_texts_print()
    elif x == "05":
        sql_search_this_person()
    elif x == "06":
        sql_search_two_persons()
    elif x == "07":
        sql_search_with_tags()
    elif x == "08":
        sql_search_news_by_tablename_date()
    else:
        print("this is not an option")




# =============> CUSTOM 

# Συνδέει "αυτόματα" ειδήσεις από τον πίνακα news_table με πρόσωπα από τον πίνακα persons_name και σώζει στα news_persons_rel
def sql_news_persons_rel():
    db = "DBs/news_05.db"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM news_table;")
    news = cursor.fetchall()
    
    cursor.execute("SELECT id, persons_name FROM persons_table;")
    persons = cursor.fetchall()

    for news_id, news_text in news:
        for person_id, person_name in persons:
            if person_name in news_text:
                cursor.execute(
                    "INSERT OR IGNORE INTO news_persons_rel (news_id, person_id) VALUES (?, ?)",
                    (news_id, person_id)
                )
                print(f"Linked person {person_name} with news id {news_id}")

    conn.commit()
    conn.close()

# Αφού κάνει scrap σε είδηση με newspaper3k προσθέτει τις τιμές στον πίνακα news (προσοχή! φιξ σε 5)
def sq_from_scrap_to_db(url):

    line = news_scrap_newspaper3k_full(url)
    sq_add_line_to_news_table(line)
    print("η είδηση προστέθηκε")
    sq_inspect_db("DBs/news_05")

# Το ίδιο αλλά το κάνει σε μια λίστα 
def sq_from_scrap_to_db_list(url_list):
    for url in url_list:
        sq_from_scrap_to_db(url)


# Αν ο τίτλος περιέχει συγκεκριμένες λέξεις, βάζει στα θέματα tags

def sql_auto_tags():
    conn, cursor = sq_db_connect_or_create(db)

    tags_keys = {
        "πολιτική" : ["βουλή", "κόμμα", "ΝΔ", "ΠΑΣΟΚ", "ΚΚΕ", "ΣΥΡΙΖΑ", "Πλεύση Ελευθερίας","Μητσοτάκης","Ανδρουλάκης","Φάμελος","Κωνσταντοπούλου"] ,
        "οικονομία" : ["ακρίβεια","οικονομία","μετοχές","κέρδος","κέρδη","ποσοστά"],
        "γεωπολιτική" : ["ΗΠΑ", "Ρωσία", "Ευρώπη", "ΕΕ", "Ουκρανία", "Γάζα", "Τραμπ", "Πούτιν","Λάιεν"] 

    }

    q = "SELECT id, title FROM news_table"
    cursor.execute(q)
    rows = cursor.fetchall()

    for news_id, title in rows:
        title_lower = title.lower()  # Για να μην έχει σημασία το κεφαλαίο/πεζό

        for tag, keywords in tags_keys.items():
            # Έλεγχος αν κάποια από τις λέξεις-κλειδιά υπάρχει στον τίτλο
            if any(kw.lower() in title_lower for kw in keywords):
                # 1. Εισαγωγή tag (αν δεν υπάρχει)
                cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
                cursor.execute("SELECT id FROM tags WHERE name=?", (tag,))
                tag_id = cursor.fetchone()[0]

                # 2. Σύνδεση είδησης με tag
                cursor.execute(
                    "INSERT OR IGNORE INTO news_tags (news_id, tag_id) VALUES (?, ?)",
                    (news_id, tag_id)
                )


    print("τα tags για πολιτική, οικονομία, γεωπολιτική προστέθηκαν στις ειδήσεις")

    conn.commit()
    conn.close()



# =============> για ταξινόμηση 

def add_relation(conn, news_title, news_date, person_name, identity, role):
    cursor = conn.cursor()

    # 1. Βρίσκουμε ή δημιουργούμε την είδηση
    cursor.execute("SELECT id FROM news_table WHERE title = ? AND date = ?", (news_title, news_date))
    row = cursor.fetchone()
    if row:
        news_id = row[0]
    else:
        cursor.execute("INSERT INTO news_table (title, date) VALUES (?, ?)", (news_title, news_date))
        news_id = cursor.lastrowid

    # 2. Βρίσκουμε ή δημιουργούμε το πρόσωπο
    cursor.execute("SELECT id FROM persons_table WHERE persons_name = ?", (person_name,))
    row = cursor.fetchone()
    if row:
        person_id = row[0]
    else:
        cursor.execute("INSERT INTO persons_table (persons_name, identity) VALUES (?, ?)", (person_name, identity))
        person_id = cursor.lastrowid

    # 3. Προσθέτουμε τη σχέση
    cursor.execute("""
        INSERT OR IGNORE INTO news_persons_rel (news_id, person_id, role)
        VALUES (?, ?, ?)
    """, (news_id, person_id, role))

    conn.commit()
    return news_id, person_id

def sq_insert_news_persons_rel(db,news_id,person_id,role):

    conn = sqlite3.connect(f"{db}.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO news_persons_rel (news_id, person_id, role) VALUES (?, ?, ?)", 
        (news_id, person_id, role))
    
    conn.commit()
    conn.close()

def get_news_by_person(db, person_name):
    """
    Επιστρέφει όλες τις ειδήσεις που συνδέονται με άτομο, 
    ανεξαρτήτως κεφαλαίων/μικρών και με μερική αντιστοίχιση.
    """
    conn = sqlite3.connect(f"{db}.db")
    cursor = conn.cursor()

    query = """
    SELECT n.title, n.date, r.role
    FROM persons_table p
    JOIN news_persons_rel r ON p.id = r.person_id
    JOIN news_table n ON n.id = r.news_id
    WHERE LOWER(p.persons_name) LIKE LOWER(?)
    """
    # Προσθέτουμε % για να βρει κάθε εμφάνιση της λέξης μέσα στο όνομα
    cursor.execute(query, (f"%{person_name}%",))
    results = cursor.fetchall()

    conn.close()
    return results
def get_persons_by_news(db, news_title):
    conn = sqlite3.connect(f"{db}.db")
    cursor = conn.cursor()

    query = """
    SELECT p.persons_name, p.identity, r.role
    FROM news_table n
    JOIN news_persons_rel r ON n.id = r.news_id
    JOIN persons_table p ON p.id = r.person_id
    WHERE n.title = ?
    """
    cursor.execute(query, (news_title,))
    results = cursor.fetchall()

    conn.close()
    return results

def link_news_to_persons(db, news_id):
    conn = sqlite3.connect(f"{db}.db")
    cursor = conn.cursor()

    # Παίρνουμε το κείμενο της είδησης
    cursor.execute("SELECT text FROM news_table WHERE id = ?", (news_id,))
    news_text = cursor.fetchone()[0]

    # Παίρνουμε όλα τα ονόματα από τον πίνακα persons_table
    cursor.execute("SELECT id, persons_name FROM persons_table")
    persons = cursor.fetchall()

    # Ελέγχουμε αν κάθε όνομα υπάρχει στο κείμενο
    for person_id, person_name in persons:
        if person_name in news_text:   # απλό string search
            cursor.execute("""
                INSERT OR IGNORE INTO news_persons_rel (news_id, person_id, role)
                VALUES (?, ?, ?)
            """, (news_id, person_id, "αναφορά"))

    conn.commit()
    conn.close()
def sq_link_last_news_to_persons(db):
    conn = sqlite3.connect(f"{db}.db")
    cursor = conn.cursor()

    # Βρίσκουμε το τελευταίο id από τον πίνακα news_table
    cursor.execute("SELECT id, text FROM news_table ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if not row:
        print("Δεν υπάρχουν ειδήσεις στη βάση.")
        conn.close()
        return

    news_id, news_text = row

    # Παίρνουμε όλα τα ονόματα από τον πίνακα persons_table
    cursor.execute("SELECT id, persons_name FROM persons_table")
    persons = cursor.fetchall()

    # Ελέγχουμε αν κάθε όνομα υπάρχει στο κείμενο
    for person_id, person_name in persons:
        if person_name in news_text:
            cursor.execute("""
                INSERT OR IGNORE INTO news_persons_rel (news_id, person_id, role)
                VALUES (?, ?, ?)
            """, (news_id, person_id, "αναφορά"))

    conn.commit()
    conn.close()
    print(f"Έγινε σύνδεση για την είδηση με id={news_id}.")




# ********************* TEST AREA *********************
# Οι πίνακες μου: news_table / news_persons_rel / persons_table / place_table / events_table / tags / news_tags
    
db = "DBs/news_05"
table_name = "tags_news_table"
columns = ["url", "title", "text"]

# sql_super_inspect()
# sql_super_search()
# sql_super_add()

'''
query = "INSERT OR IGNORE INTO tags (name) VALUES ('πολιτική'), ('οικονομία'), ('γεωπολιτικά') ;"

conn, cursor = sq_db_connect_or_create(db)
cursor.execute(query)
conn.commit()
conn.close()
'''

