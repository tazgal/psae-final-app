import streamlit as st
import json
from pathlib import Path
import uuid
from datetime import datetime

# Ρυθμίσεις
DATA_FILE = Path("data.json")
IMAGES_DIR = Path("images")
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
    return {"sections": [], "last_updated": datetime.now().isoformat()}

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

def safe_delete_image(image_path):
    """Ασφαλής διαγραφή εικόνας"""
    try:
        if image_path and Path(image_path).exists():
            Path(image_path).unlink()
            return True
    except Exception as e:
        st.error(f"Σφάλμα διαγραφής εικόνας: {e}")
    return False

def generate_unique_filename(original_name):
    """Δημιουργία μοναδικού ονόματος αρχείου"""
    ext = Path(original_name).suffix
    return f"{uuid.uuid4()}{ext}"

# ---- Αρχικοποίηση ----
data = load_data()

# ---- Sidebar για επεξεργασία ----
st.sidebar.header("🔧 Επεξεργασία Περιεχομένου")

# Επιλογή ή δημιουργία νέας ενότητας
if data["sections"]:
    selected = st.sidebar.selectbox(
        "Ενότητα", 
        range(len(data["sections"])), 
        format_func=lambda i: f"{data['sections'][i]['title']} (ID: {i+1})"
    )
    section = data["sections"][selected]
    
    st.sidebar.subheader(f"Επεξεργασία: {section['title']}")
    
    new_title = st.sidebar.text_input("Τίτλος", section["title"], key=f"title_{selected}")
    new_text = st.sidebar.text_area("Κείμενο", section["text"], key=f"text_{selected}")

    # Εμφάνιση τρέχουσας εικόνας
    if section.get("image") and Path(section["image"]).exists():
        st.sidebar.image(section["image"], caption="Τρέχουσα εικόνα")
        if st.sidebar.button("🗑️ Διαγραφή εικόνας", key=f"delete_{selected}"):
            if safe_delete_image(section["image"]):
                section["image"] = ""
                if save_data(data):
                    st.success("✅ Εικόνα διαγράφηκε!")
                    st.rerun()

    uploaded_file = st.sidebar.file_uploader(
        "Ανέβασε νέα εικόνα", 
        type=["png", "jpg", "jpeg", "gif"],
        key=f"upload_{selected}"
    )
    
    if uploaded_file:
        # Διαγραφή παλιάς εικόνας
        if section.get("image"):
            safe_delete_image(section["image"])
        
        # Αποθήκευση νέας εικόνας
        unique_filename = generate_unique_filename(uploaded_file.name)
        image_path = IMAGES_DIR / unique_filename
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        new_image = str(image_path)
        
        # Προεπισκόπηση νέας εικόνας
        st.sidebar.image(new_image, caption="Νέα εικόνα")
    else:
        new_image = section.get("image", "")

    # Κουμπιά δράσης
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("💾 Αποθήκευση", key=f"save_{selected}"):
            section["title"] = new_title
            section["text"] = new_text
            section["image"] = new_image
            if save_data(data):
                st.success("✅ Οι αλλαγές αποθηκεύτηκαν!")
                st.rerun()
    
    with col2:
        if st.button("🗑️ Διαγραφή ενότητας", key=f"delete_section_{selected}"):
            # Διαγραφή εικόνας της ενότητας
            if section.get("image"):
                safe_delete_image(section["image"])
            
            # Διαγραφή ενότητας
            data["sections"].pop(selected)
            if save_data(data):
                st.success("✅ Ενότητα διαγράφηκε!")
                st.rerun()

else:
    st.sidebar.info("📝 Δεν υπάρχουν ενότητες. Δημιούργησε μία παρακάτω.")

# ---- Δημιουργία νέας ενότητας ----
st.sidebar.markdown("---")
st.sidebar.subheader("➕ Προσθήκη Νέας Ενότητας")

new_section_title = st.sidebar.text_input("Τίτλος νέας ενότητας", key="new_title")
new_section_text = st.sidebar.text_area("Κείμενο νέας ενότητας", key="new_text")
new_uploaded_file = st.sidebar.file_uploader(
    "Ανέβασε εικόνα για νέα ενότητα", 
    type=["png", "jpg", "jpeg", "gif"], 
    key="new_img"
)

if new_uploaded_file:
    unique_filename = generate_unique_filename(new_uploaded_file.name)
    new_image_path = IMAGES_DIR / unique_filename
    with open(new_image_path, "wb") as f:
        f.write(new_uploaded_file.getbuffer())
    new_section_image = str(new_image_path)
    st.sidebar.image(new_section_image, caption="Προεπισκόπηση")
else:
    new_section_image = ""

if st.sidebar.button("➕ Προσθήκη νέας ενότητας", type="primary"):
    if new_section_title.strip():
        new_section = {
            "title": new_section_title,
            "text": new_section_text,
            "image": new_section_image,
            "created_at": datetime.now().isoformat()
        }
        data["sections"].append(new_section)
        if save_data(data):
            st.success("✅ Νέα ενότητα προστέθηκε!")
            st.rerun()
    else:
        st.sidebar.warning("⚠️ Ο τίτλος της ενότητας δεν μπορεί να είναι κενός.")

# ---- Εμφάνιση σελίδας ----
st.title("🌐 Μικρή Δυναμική Ιστοσελίδα")

# Πληροφορίες συστήματος
if data.get("last_updated"):
    last_update = datetime.fromisoformat(data["last_updated"]).strftime("%d/%m/%Y %H:%M")
    st.caption(f"Τελευταία ενημέρωση: {last_update} | Σύνολο ενοτήτων: {len(data['sections'])}")

if not data["sections"]:
    st.info("""
    🏠 **Καλώς ήρθατε!**
    
    Αυτή είναι η κύρια σελίδα σας. Για να προσθέσετε περιεχόμενο:
    1. Χρησιμοποιήστε την sidebar στα αριστερά
    2. Επιλέξτε "➕ Προσθήκη Νέας Ενότητας"
    3. Συμπληρώστε τον τίτλο και το κείμενο
    4. Προσθέστε εικόνα (προαιρετικά)
    5. Κάντε κλικ στο κουμπί "➕ Προσθήκη"
    """)
else:
    for idx, section in enumerate(data["sections"]):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {section['title']}")
            with col2:
                st.caption(f"Ενότητα {idx + 1}")
            
            if section.get("image") and Path(section["image"]).exists():
                st.image(section["image"])
            
            st.markdown(section["text"])
            
            if section.get("created_at"):
                created_date = datetime.fromisoformat(section["created_at"]).strftime("%d/%m/%Y")
                st.caption(f"Δημιουργήθηκε: {created_date}")
            
            st.markdown("---")

# ---- Στατιστικά ----
if st.sidebar.checkbox("📊 Στατιστικά"):
    st.sidebar.subheader("Στατιστικά")
    total_sections = len(data["sections"])
    sections_with_images = len([s for s in data["sections"] if s.get("image")])
    
    st.sidebar.metric("Σύνολο Ενοτήτων", total_sections)
    st.sidebar.metric("Ενότητες με Εικόνες", sections_with_images)
    
    if total_sections > 0:
        st.sidebar.progress(sections_with_images / total_sections, 
                          text=f"Ενότητες με εικόνες: {sections_with_images/total_sections*100:.1f}%")