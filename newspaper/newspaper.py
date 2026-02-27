import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid

# Ρυθμίσεις
DATA_FILE = Path("newspaper_data.json")
IMAGES_DIR = Path("newspaper_images")
IMAGES_DIR.mkdir(exist_ok=True)

# ---- Βοηθητικές συναρτήσεις ----
def load_data():
    """Φόρτωση δεδομένων από JSON αρχείο"""
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης δεδομένων: {e}")
    return {
        "logo": "",
        "main_news": {"title": "", "image": "", "text": ""},
        "bottom_text": "",
        "left_column": [],
        "right_article": {"title": "", "text": ""},
        "last_updated": datetime.now().isoformat()
    }

def save_data(data):
    """Αποθήκευση δεδομένων σε JSON αρχείο"""
    try:
        data["last_updated"] = datetime.now().isoformat()
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Σφάλμα αποθήκευσης: {e}")
        return False

def save_uploaded_file(uploaded_file):
    """Αποθήκευση ανεβασμένου αρχείου"""
    try:
        if uploaded_file is not None:
            # Δημιουργία μοναδικού ονόματος
            file_extension = Path(uploaded_file.name).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            image_path = IMAGES_DIR / unique_filename
            
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return str(image_path)
    except Exception as e:
        st.error(f"Σφάλμα αποθήκευσης αρχείου: {e}")
    return ""

# ---- Αρχικοποίηση ----
data = load_data()

# ---- Streamlit Εφαρμογή ----
st.set_page_config(page_title="Εφημερίδα", layout="wide")

# Sidebar για επεξεργασία
st.sidebar.title("📰 Σύνταξη Εφημερίδας")

# 1. Λογότυπο
st.sidebar.header("1. Λογότυπο")
logo_file = st.sidebar.file_uploader("Επιλογή λογότυπου", type=["png", "jpg", "jpeg"], key="logo")
if logo_file:
    logo_path = save_uploaded_file(logo_file)
    if logo_path:
        data["logo"] = logo_path
        save_data(data)

if st.sidebar.button("🗑️ Διαγραφή λογότυπου"):
    data["logo"] = ""
    save_data(data)

# 2. Κεντρικό Θέμα
st.sidebar.header("2. Κεντρικό Θέμα")
main_title = st.sidebar.text_input("Τίτλος κεντρικού θέματος", value=data["main_news"]["title"])
main_image_file = st.sidebar.file_uploader("Εικόνα κεντρικού θέματος", type=["png", "jpg", "jpeg"], key="main_image")
if main_image_file:
    main_image_path = save_uploaded_file(main_image_file)
    if main_image_path:
        data["main_news"]["image"] = main_image_path
        save_data(data)

main_text = st.sidebar.text_area("Κείμενο κεντρικού θέματος", value=data["main_news"]["text"], height=100)

if st.sidebar.button("💾 Αποθήκευση κεντρικού θέματος"):
    data["main_news"]["title"] = main_title
    data["main_news"]["text"] = main_text
    save_data(data)

# 3. Αριστερή Στήλη - Ανακοινώσεις
st.sidebar.header("3. Ανακοινώσεις (Αριστερά)")
new_announcement = st.sidebar.text_input("Νέα ανακοίνωση")
if st.sidebar.button("➕ Προσθήκη ανακοίνωσης"):
    if new_announcement.strip():
        data["left_column"].append(new_announcement)
        save_data(data)

# Εμφάνιση και διαχείριση ανακοινώσεων
if data["left_column"]:
    st.sidebar.write("Υπάρχουσες ανακοινώσεις:")
    for i, announcement in enumerate(data["left_column"]):
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.sidebar.write(f"• {announcement}")
        with col2:
            if st.sidebar.button("🗑️", key=f"del_ann_{i}"):
                data["left_column"].pop(i)
                save_data(data)
                st.rerun()

# 4. Δεξιά Στήλη - Άρθρο
st.sidebar.header("4. Άρθρο (Δεξιά)")
right_title = st.sidebar.text_input("Τίτλος άρθρου", value=data["right_article"]["title"])
right_text = st.sidebar.text_area("Κείμενο άρθρου (~200 λέξεις)", value=data["right_article"]["text"], height=150)

# Μετρητής λέξεων
if right_text:
    word_count = len(right_text.split())
    st.sidebar.write(f"Λέξεις: {word_count}/200")
    if word_count > 200:
        st.sidebar.warning("Το κείμενο υπερβαίνει τις 200 λέξεις!")

if st.sidebar.button("💾 Αποθήκευση άρθρου"):
    data["right_article"]["title"] = right_title
    data["right_article"]["text"] = right_text
    save_data(data)

# 5. Κειμενολεζάντα
st.sidebar.header("5. Κειμενολεζάντα (Βάση)")
bottom_text = st.sidebar.text_area("Κειμενολεζάντα", value=data["bottom_text"], height=80)
if st.sidebar.button("💾 Αποθήκευση κειμενολεζάντας"):
    data["bottom_text"] = bottom_text
    save_data(data)

# ---- ΕΜΦΑΝΙΣΗ ΕΦΗΜΕΡΙΔΑΣ ----

# Χρώματα και στυλ
st.markdown("""
<style>
    .newspaper-title {
        font-family: 'Arial', serif;
        font-size: 3em;
        text-align: center;
        margin-bottom: 20px;
    }
    .main-news-title {
        font-family: 'Arial', serif;
        font-size: 2em;
        text-align: center;
        margin: 20px 0;
    }
    .section-title {
        font-family: 'Arial', serif;
        font-size: 1.5em;
        border-bottom: 2px solid #000;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    .announcement-item {
        font-family: Arial, sans-serif;
        font-size: 0.9em;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    .article-text {
        font-family: 'Arial', serif;
        font-size: 1em;
        line-height: 1.6;
        text-align: justify;
    }
    .bottom-text {
        font-family: Arial, sans-serif;
        font-size: 0.8em;
        text-align: center;
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)

# Κύρια σελίδα
st.markdown('<div class="newspaper-title"></div>', unsafe_allow_html=True)

# Λογότυπο
if data["logo"]:
    st.image(data["logo"])

# Κύρια διάταξη με 3 columns
col1, col2, col3 = st.columns([1, 2, 1])

# ΑΡΙΣΤΕΡΗ ΣΤΗΛΗ - Ανακοινώσεις
with col1:
    st.markdown('<div class="section-title"></div>', unsafe_allow_html=True)
    
    if data["left_column"]:
        for announcement in data["left_column"]:
            st.markdown(f'<div class="announcement-item">• {announcement}</div>', unsafe_allow_html=True)
    else:
        st.info("Δεν υπάρχουν ανακοινώσεις")
        st.markdown('<div class="announcement-item">• Προστέστε ανακοινώσεις από το sidebar</div>', unsafe_allow_html=True)

# ΚΕΝΤΡΙΚΗ ΣΤΗΛΗ - Κύριο θέμα
with col2:
    st.markdown('<div class="section-title"></div>', unsafe_allow_html=True)
    
    if data["main_news"]["image"]:
        st.image(data["main_news"]["image"])
    
    if data["main_news"]["title"]:
        st.markdown(f'<div class="main-news-title">{data["main_news"]["title"]}</div>', unsafe_allow_html=True)
    
    if data["main_news"]["text"]:
        st.markdown(f'<div class="article-text">{data["main_news"]["text"]}</div>', unsafe_allow_html=True)

# ΔΕΞΙΑ ΣΤΗΛΗ - Άρθρο
with col3:
    st.markdown('<div class="section-title">Η ΑΠΟΨΗ ΜΑΣ</div>', unsafe_allow_html=True)
    
    if data["right_article"]["title"]:
        st.subheader(data["right_article"]["title"])
    
    if data["right_article"]["text"]:
        st.markdown(f'<div class="article-text">{data["right_article"]["text"]}</div>', unsafe_allow_html=True)
    else:
        st.info("Δεν υπάρχει άρθρο")
        st.markdown('<div class="article-text">Προσθέστε ένα άρθρο περίπου 200 λέξεων από το sidebar.</div>', unsafe_allow_html=True)

# ΚΕΙΜΕΝΟΛΕΖΑΝΤΑ - Στο κάτω μέρος
if data["bottom_text"]:
    st.markdown("---")
    st.markdown(f'<div class="bottom-text">{data["bottom_text"]}</div>', unsafe_allow_html=True)

# Πληροφορίες
st.sidebar.markdown("---")
st.sidebar.info("""
**Οδηγίες χρήσης:**
1. Προσθέστε λογότυπο
2. Συμπληρώστε το κεντρικό θέμα
3. Προσθέστε ανακοινώσεις αριστερά
4. Γράψτε το άρθρο δεξιά (~200 λέξεις)
5. Προσθέστε κειμενολεζάντα
""")

# Κουμπί επαναφοράς
if st.sidebar.button("🔄 Επαναφορά όλων"):
    if st.sidebar.confirm("Είστε σίγουρος ότι θέλετε να διαγράψετε όλο το περιεχόμενο;"):
        DATA_FILE.unlink(missing_ok=True)
        st.rerun()