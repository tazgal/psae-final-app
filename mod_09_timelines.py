# ********************* ΒΙΒΛΙΟΘΗΚΕΣ *********************


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# ********************* DEFS *********************


# Δείχνει απλά με μια τελεία την είδηση 
def tml_plt_show_news():
    conn = sqlite3.connect("news_05.db")
    query = "SELECT date, title FROM news_table WHERE date IS NOT NULL ORDER BY date Desc"
    df = pd.read_sql_query(query,conn)

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    # Πετάμε όσα NaT
    df = df.dropna(subset=["date"])

    # Φτιάχνουμε scatter με τις ημερομηνίες
    plt.figure(figsize=(12,6))
    plt.scatter(df["date"], [1]*len(df), marker="o")


    # Προσθέτουμε labels (τίτλους)
    for i, row in df.iterrows():
        plt.text(row["date"], 1.02, row["title"], rotation = 90, ha="left", fontsize=8)

    plt.show()

# Ψάχνει σε τίτλους με λέξη κλειδί και βάζει την είδηση σε ένα διάγραμμα με ημερομηνίες
def tml_plt_search_titles_show_news():
    conn = sqlite3.connect("news_05.db")
    keyword = input("pls enter keyword to search ")
    query = f"SELECT date, title FROM news_table WHERE date IS NOT NULL AND title LIKE '%{keyword}%' ORDER BY date Desc"
    df = pd.read_sql_query(query,conn)

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    # Πετάμε όσα NaT
    df = df.dropna(subset=["date"])

    # Φτιάχνουμε scatter με τις ημερομηνίες
    plt.figure(figsize=(12,6))
    plt.scatter(df["date"], [1]*len(df), marker="o")


    # Προσθέτουμε labels (τίτλους)
    for i, row in df.iterrows():
        plt.text(row["date"], 1.02, row["title"], rotation = 90, ha="left", fontsize=8)

    plt.show()

def tml_from_csv_to_scatterplot():
    csv_path = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/Test_timeline.csv"
    df = pd.read_csv(csv_path)

    # Μετονομασία των στηλών για ευκολία (αν θέλουμε)
    df = df.rename(columns={"Date": "date", "Title": "title", "Topic": "topic"})

    # Μετατροπή της στήλης date σε τύπο datetime
    df['date'] = pd.to_datetime(df['date'])

    # Ταξινόμηση κατά ημερομηνία    
    df = df.sort_values('date')

    # Δημιουργία scatter plot: x=ημερομηνία, y=κατηγορία (topic)
    # Θα εμφανιστούν διαφορετικά χρώματα ανά topic
    plt.figure(figsize=(10,6))
    topics = df['topic'].unique()

    for t in topics:
        subset = df[df['topic']==t]
        plt.scatter(subset['date'], [t]*len(subset), label=t)

    plt.xlabel("Ημερομηνία")
    plt.ylabel("Θέμα (topic)")
    plt.title("Χρονολογική απεικόνιση ειδήσεων ανά θεματική κατηγορία")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # εδώ το κάνουμε διαδραστικό 
    fig = px.scatter(
        df,
        x="date",
        y="topic",
        hover_data=["title"],   # Εμφάνιση τίτλων στο hover
        color="topic",
        title="Ειδήσεις ανά Θεματική Κατηγορία στον Χρόνο"
    )

    fig.update_layout(
        xaxis_title="Ημερομηνία",
        yaxis_title="Θεματική Κατηγορία",
        legend_title="Topic"
    )

    fig.show()



# ********************* TEST AREA *********************

