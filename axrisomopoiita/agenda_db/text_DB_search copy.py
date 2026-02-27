import sqlite3
import os 

'''
conn = sqlite3.connect('test.db')
print("Opened database successfully")

cursor = conn.cursor()

q = "CREATE TABLE texts (Id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT);"
cursor.execute(q)
print("Table texts created successfully")

conn.commit()

q2 = "CREATE TABLE persons (Id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);"
cursor.execute(q2)
print("Table persons created successfully")

conn.commit()

q3 = "CREATE TABLE places (Id INTEGER PRIMARY KEY AUTOINCREMENT, place TEXT);"
cursor.execute(q3)
print("Table places created successfully")

conn.commit()
'''

# ********** Συναρτήσεις **********

def open_text_sp(file):
    with open(f"{file}.txt", "r", encoding="utf-8") as f:
        content = f.read()
        return content

# Ανοίγει τα αρχεία από τον συγκεκριμένο φάκελο (Προσοχή! πρέπει να μπαίνει το σωστό dir)
def open_files_from_folder():
    folder = "/Users/tazgal/project_db"
    os.chdir(f"{folder}")

    files = []

    for file in os.listdir(folder):  # παίρνουμε όλα τα αρχεία
        print("Found:", file)  # εμφάνιση ονόματος

        if file.endswith(".txt"):
            filename_without_ext = os.path.splitext(file)[0]  # κόβει το ".txt"
            text = open_text_sp(filename_without_ext)
            files.append(text)
    
    for file in files:
        print(file)
        print("**************")
    return files        

# βάζει κείμενο στη ΒΔ (στον πίνακα με το κείμενο)
def add_to_db(import_text):
  conn = sqlite3.connect('test.db')
  print("Opened database successfully")
  cursor = conn.cursor()

  query = "INSERT OR IGNORE INTO texts (text) VALUES (?)"
  cursor.execute(query, (import_text,))

  conn.commit()
  print("το κείμενο προστέθηκε")
  conn.close()

# ανοίγει txt παίρνει το κείμενο και το σώζει στη ΒΔ
def open_text_save_to_db(path):
  with open(f"{path}.txt", "r", encoding="utf-8") as f:
    text = f.read()
    add_to_db(text)

# Σου δείχνει (όλα) τα αποθηκευμένα κείμενα
def show_texts():
  conn = sqlite3.connect('test.db')
  print("Opened database successfully")
  cursor = conn.cursor()
  q4 = "SELECT * FROM texts"
  x = cursor.execute(q4)
  texts = x.fetchall()

  print(texts)
  return texts

# Βάζεις λέξη κλειδί και σου επιστρέφει τα κείμενα στα οποία αυτή περιέχεται 
def filter_results():
  conn = sqlite3.connect('test.db')
  print("Opened database successfully")
  cursor = conn.cursor()

  key = input("pls enter keyword ").strip()
  key2 = f"%{key}%"


  query = "SELECT text FROM texts WHERE text LIKE ?"
  cursor.execute(query, (key2,))
  rows = cursor.fetchall()

  results = [row[0] for row in rows]

  print(f"Η λέξη {key} βρίσκεται στα εξής κείμενα")

  for result in results:
    print(result)
    print("********************")

  conn.close()

  return results

# Αν θες να σώσεις τα αποτελέσματα για κάτι που ψάχνεις σου ανοίγει ένα αρχείο txt και βάζει εκεί τα κείμενα
def write_new_txt(x):
    name = input("Βάλτε όνομα που θα έχει το αρχείο σας ").strip()
    with open(f"{name}.txt", "a", encoding="utf-8") as f:
        for i in x:
            f.write(i + "\n")

# Μια ενιαία: ανοίγει τα κείμενα που βρίσκονται στο φάκελο, αν δεν υπάρχουν τα σώζει στη ΒΔ και τα τυπώνει
def open_files_save_to_db():
    texts = open_files_from_folder()
    for text in texts:
        add_to_db(text)
    results = show_texts()
    for r in results:
        print(r)
        print("\n\n")


