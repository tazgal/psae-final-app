import sqlite3


# Python functions

def get_conn(db="news_demo.db"):
    return sqlite3.connect(db)

# Δημιουργία των πινάκων
def create_tables():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS news_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        url TEXT UNIQUE
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS persons_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persons_name TEXT UNIQUE,
        identity TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS news_persons (
        news_id INTEGER,
        person_id INTEGER,
        PRIMARY KEY (news_id, person_id),
        FOREIGN KEY (news_id) REFERENCES news_table(id),
        FOREIGN KEY (person_id) REFERENCES persons_table(id)
    )""")
    conn.commit()
    conn.close()


# Εισαγωγή είδησης
def insert_news(title, date, url):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO news_table (title, date, url) VALUES (?, ?, ?)", 
                (title, date, url))
    conn.commit()
    news_id = cur.execute("SELECT id FROM news_table WHERE url=?", (url,)).fetchone()[0]
    conn.close()
    return news_id

# Εισαγωγή προσώπου
def insert_person(name, identity=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO persons_table (persons_name, identity) VALUES (?, ?)", 
                (name, identity))
    conn.commit()
    person_id = cur.execute("SELECT id FROM persons_table WHERE persons_name=?", (name,)).fetchone()[0]
    conn.close()
    return person_id

# Σύνδεση προσώπου με είδηση
def link_person_to_news(news_id, person_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO news_persons (news_id, person_id) VALUES (?, ?)", 
                (news_id, person_id))
    conn.commit()
    conn.close()

create_tables()

news1 = insert_news("Συνάντηση κορυφής ΗΠΑ - Ρωσίας", "2025-08-20", "http://example.com/news1")
putin = insert_person("Βλαντιμίρ Πούτιν", "Πρόεδρος Ρωσίας")
biden = insert_person("Τζο Μπάιντεν", "Πρόεδρος ΗΠΑ")

link_person_to_news(news1, putin)
link_person_to_news(news1, biden)
