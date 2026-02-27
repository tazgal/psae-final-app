import streamlit as st
from mod_02_scrap import scrap_news_return_links2
from mod_05_sql import sq_from_scrap_to_db, sq_link_last_news_to_persons,sq_db_connect_or_create,sq_search_and_return_texts,sql_auto_tags
from mod_08_geo import geo_spacy_coordinates, geo_dict_all_new_el,geo_list_all_el, fol_pin_list

# 1. Κάνει σκραπ ειδήσεις από συγκεκριμένες ιστοσελίδες με λέξεις κλειδιά (με requests και όχι με newspaper3k)
# 2. Σώζει σε μια ΒΔ στο table news και διασυνδέει με table για πρόσωπα
# 3. Τυπώνει τους τίτλους των ειδήσεων

def scr_from_news_to_db_and_persons():
    db = "news_05"
    ch = input("διαλέξτε κατηγορία για scraping ")
    urls = scrap_news_return_links2(ch)

    for url in set(urls):
        sq_from_scrap_to_db(url)
        sq_link_last_news_to_persons(db)

    conn, cursor = sq_db_connect_or_create(db)
    query = ("SELECT title FROM news_table")
    cursor.execute(query)

    rows = cursor.fetchall()   # φέρνει όλες τις σειρές
    for r in rows:
        print(r[0])  # r[0] = το πεδίο title

    conn.commit()
    conn.close()

# Το ίδιο + βάζει αυτόματα 3 tags ανάλογα με το τι περιέχεται στον τίτλο 

def scr_from_news_to_db_and_persons2():
    db = "news_05"
    ch = input("διαλέξτε κατηγορία για scraping ")
    urls = scrap_news_return_links2(ch)

    for url in set(urls):
        sq_from_scrap_to_db(url)
        sq_link_last_news_to_persons(db)

    conn, cursor = sq_db_connect_or_create(db)
    query = ("SELECT title FROM news_table")
    cursor.execute(query)

    counter = 0

    rows = cursor.fetchall()   # φέρνει όλες τις σειρές
    for r in rows:
        print(r[0])  # r[0] = το πεδίο title
        counter = counter + 1
    
    print(f"η ΒΔ σου περιέχει τώρα {counter} ειδήσεις")
    sql_auto_tags()

    conn.commit()
    conn.close()

#Το ίδιο, αλλά κάνει μόνο του τις κατηγορίες
def scr_from_news_to_db_and_persons3():
    db = "news_05"
    
    # Αντί για input, τρέχουμε όλες τις επιλογές
    categories = ["1", "2", "3"]

    for ch in categories:
        print(f"Scraping για κατηγορία {ch}...")
        urls = scrap_news_return_links2(ch)

        for url in set(urls):
            sq_from_scrap_to_db(url)
            sq_link_last_news_to_persons(db)

    # Συνέχεια με το υπόλοιπο
    conn, cursor = sq_db_connect_or_create(db)
    query = ("SELECT title FROM news_table")
    cursor.execute(query)

    counter = 0
    rows = cursor.fetchall()   # φέρνει όλες τις σειρές
    for r in rows:
        print(r[0])  # r[0] = το πεδίο title
        counter += 1
    
    print(f"η ΒΔ σου περιέχει τώρα {counter} ειδήσεις")
    sql_auto_tags()

    conn.commit()
    conn.close()


def scr_from_news_to_db_and_persons3_streamlit():
    db = "DBs/news_05"
    
    # Αντί για input, τρέχουμε όλες τις επιλογές
    categories = ["1", "2", "3"]

    for ch in categories:
        print(f"Scraping για κατηγορία {ch}...")
        urls = scrap_news_return_links2(ch)

        for url in set(urls):
            sq_from_scrap_to_db(url)
            sq_link_last_news_to_persons(db)

    # Συνέχεια με το υπόλοιπο
    conn, cursor = sq_db_connect_or_create(db)
    query = ("SELECT title FROM news_table")
    cursor.execute(query)

    counter = 0
    rows = cursor.fetchall()   # φέρνει όλες τις σειρές
    for r in rows:
        print(r[0])  # r[0] = το πεδίο title
        counter += 1
    
    st.write(f"η ΒΔ σου περιέχει τώρα {counter} ειδήσεις")
    sql_auto_tags()

    conn.commit()
    conn.close()


# 1. Κάνει search με λέξη κλειδί στο κείμενο των ειδήσεων στη ΒΔ
# 2. "Τραβάει" από εξωτερικό λεξικό συντεταγμένες και τις κολλάει σε ανάλογες οντότητες που η Spacy αναγνωρίζει ως GPE 
# 3. Προβάλει με folium τις σχετικές πινέζες στο χάρτη 

def scr_from_db_to_map():
    newstext = sq_search_and_return_texts()
    x = geo_spacy_coordinates(newstext, geo_dict_all_new_el)
    fol_pin_list(x)

# ********************* TEST AREA *********************

# scr_from_news_to_db_and_persons()
#scr_from_db_to_map()
#scr_from_news_to_db_and_persons2()
#scr_from_news_to_db_and_persons3()

