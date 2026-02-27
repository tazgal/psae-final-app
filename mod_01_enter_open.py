import os
import streamlit as st
from pathlib import Path
import streamlit as st
from docx import Document
import pandas as pd
from PIL import Image
import pdfplumber



#Σώσιμο και επιστροφή urls
def enter_url():
    url = input("Please enter url: ")
    url = f"{url}"
    return url 


def enter_urls(): 
    urls_list = []
    urls = input("Please enter urls separated by comma")
    urls = urls.split(",")
    for url in urls:
        url = url.strip()
        urls_list.append(url)
    print(urls_list)
    return urls_list

def urls_to_list(raw_text):
    # Σπάμε το input σε γραμμές και αφαιρούμε κενά και κόμματα
    lines = [line.strip().rstrip(',') for line in raw_text.strip().splitlines() if line.strip()]
    return lines  # λίστα, όχι string

# Ανοίγω ένα αρχείο txt (συγκεκριμένο)
def open_text():
    x = input("Βάλτε το όνομα του αρχείου σας")
    with open(f"{x}.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
        return content

def add_text():
    x = input("Βάλτε το όνομα του αρχείου σας")
    added_text = input("Εδώ βάλτε το κείμενο που θέλετε να προσθέσετε")

    with open(f"{x}.txt", "a", encoding="utf-8") as f:
        content = f.write(f"\n{added_text}")
        print(content)
        return content
    

#Τα ίδια αλλά με παράμετρο (που σημαίνει ότι το input το βάζω εξωτερικά)

def open_text_sp(file):
    with open(f"{file}.txt", "r", encoding="utf-8") as f:
        content = f.read()
        return content

def add_text_sp(file):
    added_text = input("Εδώ βάλτε το κείμενο που θέλετε να προσθέσετε")

    with open(f"{file}.txt", "a", encoding="utf-8") as f:
        content = f.write(f"\n{added_text}")
        return content

def add_this_to_text(x, added_text):
    
    with open(f"{x}.txt", "a", encoding="utf-8") as f:
        content = f.write(added_text)
        print(added_text)
        return content

# Καθαρίζω από λεξικό και κρατάει μια λίστα με τα urls     
def extract_only_urls(news_links):
    """
    Παίρνει λίστα από dicts [{Website, Title, Link}, ...]
    και επιστρέφει μόνο καθαρή λίστα URLs [url1, url2, ...].
    """
    urls = []
    for item in news_links:
        if isinstance(item, dict) and "Link" in item:
            urls.append(item["Link"])
    return urls

# Προσθέτει σε μια λίστα ένα ένα 
def add_to_list_one_by_one():
    urls = [] 
    while True:
        x = input("1. για URL, 2. για stop ")
        if x == "1":
            url = input("Δώσε URL: ").strip()
            urls.append(url)
            print(f"URL '{url}' προστέθηκε")
        elif x == "2":
            break
        else:
            print("Μη έγκυρη επιλογή")
    
    return urls



def add_text_agenda_streamlit(text):
    with open("σημειωματάριο.txt", "a", encoding="utf-8") as f:
        content = f.write("\n" + text)
        return True

def add_text_shmeioseis_streamlit(text):
    with open("data/texts/σημειώσεις.txt", "a", encoding="utf-8") as f:
        content = f.write("\n" + text)
        return True
    

def create_txt_and_write():
    print("Δημιουργήστε ένα νέο txt αρχείο")
    file_name = input("Δώστε όνομα στο αρχείο: ")
    text_to_add = input("Προσθέστε κείμενο: ")

    # ### ΕΛΕΓΧΟΣ / ΔΗΜΙΟΥΡΓΙΑ ΑΡΧΕΙΟΥ ###
    full_path = f"{file_name}.txt"

    # Αν δεν υπάρχει το αρχείο, δημιουργείται κενό
    if not os.path.exists(full_path):
        open(full_path, "w", encoding="utf-8").close()

    # Γράψιμο (append) στο τέλος
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(text_to_add + "\n")

    print(f"Το κείμενο προστέθηκε στο {full_path}")



def create_or_append_txt_streamlit(file_name,text_to_add):
    if not file_name:
        st.error("Παρακαλώ δώστε όνομα αρχείου.")
        return
    full_path = f"data/texts/{file_name}.txt"

    # Αν δεν υπάρχει το αρχείο, δημιουργείται κενό
    if not os.path.exists(full_path):
        open(full_path, "w", encoding="utf-8").close()

    # Προσθήκη κειμένου στο τέλος
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(text_to_add + "\n")

    st.success(f"Το κείμενο αποθηκεύτηκε στο {full_path}")

########## για 



def open_file_from_folder(folder_path: str):
    st.subheader("Επιλογή αρχείου")

    # Επιτρεπτές επεκτάσεις
    allowed_ext = (".txt", ".docx", ".csv", ".jpg", ".jpeg", ".png", ".webp",".pdf")

    try:
        files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(allowed_ext)
        ]
    except FileNotFoundError:
        st.error(f"Ο φάκελος δεν βρέθηκε: {folder_path}")
        return

    if not files:
        st.warning("Δεν βρέθηκαν αρχεία")
        return

    selected_file = st.selectbox(
        "Διάλεξε αρχείο",
        files
    )

    file_path = os.path.join(folder_path, selected_file)

    st.divider()

    # TXT
    if selected_file.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        st.text_area("Περιεχόμενο", content, height=400)

    # DOCX
    elif selected_file.endswith(".docx"):
        doc = Document(file_path)
        content = "\n".join([p.text for p in doc.paragraphs])
        st.text_area("Περιεχόμενο", content, height=400)

    # CSV
    elif selected_file.endswith(".csv"):
        df = pd.read_csv(file_path)
        st.dataframe(df)

    # ΕΙΚΟΝΕΣ
    elif selected_file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        image = Image.open(file_path)
        st.image(image, caption=selected_file, use_column_width=True)
    
    # PDF
    elif selected_file.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"

        if text.strip():
            st.text_area("Περιεχόμενο PDF", text, height=500)
        else:
            st.warning("Δεν βρέθηκε αναγνώσιμο κείμενο στο PDF")

    else:
        st.info("Μη υποστηριζόμενος τύπος αρχείου")

def dataframe_explorer2(folder: str,):

    # ---------- LOAD DATA ----------
    files = [f for f in os.listdir(folder) if f.lower().endswith((".csv", ".xlsx", ".xls"))]

    source = st.radio(
        "Data Source",
        ["📂 My files", "⬆ Upload file"],
        horizontal=True
    )

    df = None

    if source == "📂 My files":
        if not files:
            st.warning("Δεν βρέθηκαν CSV/Excel στον φάκελο")
            return

        selected = st.selectbox("Choose CSV/Excel", files)
        path = os.path.join(folder, selected)
        if selected.lower().endswith(".csv"):
            df = pd.read_csv(path)
        elif selected.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(path)

    else:
        uploaded = st.file_uploader(
            "Ανέβασε CSV ή Excel",
            type=["csv", "xlsx"]
        )

        if uploaded:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)

    if df is None:
        return

    # ---------- EDIT DATA ----------
    st.subheader("✏️ Change data")

    df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor"
    )

    return df

def dataframe_explorer3(folder: str, key_prefix="dfx"):

    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith((".csv", ".xlsx", ".xls"))
    ]

    source = st.radio(
        "Data Source",
        ["📂 My files", "⬆ Upload file"],
        horizontal=True,
        key=f"{key_prefix}_source"
    )

    df = None

    if source == "📂 My files":
        if not files:
            st.warning("Δεν βρέθηκαν CSV/Excel στον φάκελο")
            return None

        selected = st.selectbox(
            "Choose CSV/Excel",
            files,
            key=f"{key_prefix}_selectbox"
        )

        path = os.path.join(folder, selected)

        if selected.lower().endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

    else:
        uploaded = st.file_uploader(
            "Ανέβασε CSV ή Excel",
            type=["csv", "xlsx"],
            key=f"{key_prefix}_uploader"
        )

        if uploaded:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)

    if df is None:
        return None

    st.subheader("✏️ Change data")

    df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"{key_prefix}_editor"
    )

    return df
