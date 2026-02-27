
import base64
import os
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from PIL import Image
import io
from streamlit_pdf_viewer import pdf_viewer
import tempfile
import streamlit.components.v1 as components

# Προσπάθεια εισαγωγής natural_pdf (αν υπάρχει)
try:
    from natural_pdf import PDF
    NATURAL_PDF_AVAILABLE = True
except ImportError:
    NATURAL_PDF_AVAILABLE = False
    st.warning("Η βιβλιοθήκη natural_pdf δεν είναι διαθέσιμη. Ορισμένες λειτουργίες μπορεί να μην λειτουργούν.")

def pdf_open_streamlit(pdf_path):
    """Συνάρτηση που χρησιμοποιεί μόνο PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text
    except Exception as e:
        st.error(f"Σφάλμα ανάγνωσης PDF: {e}")
        return ""

def extract_tables_from_pdf(pdf_path):
    """Εξαγωγή πινάκων από PDF"""
    tables = []
    
    if NATURAL_PDF_AVAILABLE:
        try:
            pdf = PDF(pdf_path)
            for i, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        tables.append({
                            "page": i + 1,
                            "table": table
                        })
        except Exception as e:
            st.error(f"Σφάλμα με natural_pdf: {e}")
    
    # Εναλλακτική με PyMuPDF (για εικόνες πινάκων)
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Αναζήτηση για εικόνες που μπορεί να είναι πίνακες
            image_list = page.get_images()
            if image_list:
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    tables.append({
                        "page": page_num + 1,
                        "image": image_bytes,
                        "type": "image_table"
                    })
        doc.close()
    except Exception as e:
        st.error(f"Σφάλμα εξαγωγής εικόνων: {e}")
    
    return tables

def extract_images_from_pdf(pdf_path):
    """Εξαγωγή εικόνων από PDF"""
    images = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                images.append({
                    "page": page_num + 1,
                    "index": img_index,
                    "image_bytes": image_bytes,
                    "format": image_ext,
                    "size": len(image_bytes)
                })
        
        doc.close()
    except Exception as e:
        st.error(f"Σφάλμα εξαγωγής εικόνων: {e}")
    
    return images

# Κύρια εφαρμογή Streamlit


st.set_page_config(layout="wide")
st.title("📄 Προχωρημένος PDF Viewer & Extractor")

st.subheader("Open PDF from folder")

col1, col2 = st.columns([3, 1], gap="medium")

folder_path = "data/economy_files/economy_pdfs"

with col2:
    st.subheader("📂 Επιλογή Αρχείου")
    
    # Επιβεβαιώνει ότι ο φάκελος υπάρχει
    if not os.path.exists(folder_path):
        st.error(f"Ο φάκελος δεν βρέθηκε: {folder_path}")
        st.info("Δημιουργία φακέλου...")
        os.makedirs(folder_path, exist_ok=True)
        files = []
    else:
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    
    if not files:
        st.warning("Δεν βρέθηκαν αρχεία PDF στον φάκελο")
        selected_file = None
    else:
        selected_file = st.selectbox("Επιλογή αρχείου PDF", files, index=0)
    
    st.markdown("---")
    
    # ΚΟΥΜΠΙΑ ΕΞΑΓΩΓΗΣ
    st.subheader("🛠️ Εξαγωγή Περιεχομένου")
    
    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        
        # Κουμπί εξαγωγής πινάκων
        if st.button("📊 Εξαγωγή Πινάκων", use_container_width=True):
            with st.spinner("Αναζήτηση πινάκων..."):
                tables = extract_tables_from_pdf(file_path)
                
                if tables:
                    st.success(f"Βρέθηκαν {len(tables)} πίνακες/εικόνες")
                    
                    for i, table_data in enumerate(tables):
                        with st.expander(f"Πίνακας {i+1} - Σελίδα {table_data['page']}"):
                            if 'table' in table_data:
                                # Αν είναι δομημένος πίνακας
                                df = pd.DataFrame(table_data['table'])
                                st.dataframe(df, use_container_width=True)
                                
                                # Λήψη ως CSV
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label=f"📥 Λήψη Πίνακα {i+1} ως CSV",
                                    data=csv,
                                    file_name=f"table_{i+1}_page_{table_data['page']}.csv",
                                    mime="text/csv",
                                    key=f"csv_{i}"
                                )
                            elif 'image' in table_data:
                                # Αν είναι εικόνα πίνακα
                                st.image(table_data['image'], caption=f"Εικόνα πίνακα - Σελίδα {table_data['page']}")
                else:
                    st.warning("Δεν βρέθηκαν πίνακες στο PDF")
        
        # Κουμπί εξαγωγής εικόνων
        if st.button("🖼️ Εξαγωγή Εικόνων", use_container_width=True):
            with st.spinner("Εξαγωγή εικόνων..."):
                images = extract_images_from_pdf(file_path)
                
                if images:
                    st.success(f"Βρέθηκαν {len(images)} εικόνες")
                    
                    # Ομαδοποίηση ανά σελίδα
                    from collections import defaultdict
                    images_by_page = defaultdict(list)
                    
                    for img in images:
                        images_by_page[img['page']].append(img)
                    
                    for page_num, page_images in images_by_page.items():
                        with st.expander(f"Σελίδα {page_num} ({len(page_images)} εικόνες)"):
                            cols = st.columns(2)
                            for idx, img in enumerate(page_images):
                                col = cols[idx % 2]
                                with col:
                                    pil_image = Image.open(io.BytesIO(img['image_bytes']))
                                    col.image(pil_image, caption=f"Εικόνα {img['index']+1}")
                                    
                                    # Λήψη εικόνας
                                    st.download_button(
                                        label=f"📥 Λήψη",
                                        data=img['image_bytes'],
                                        file_name=f"page_{page_num}_img_{img['index']+1}.{img['format']}",
                                        mime=f"image/{img['format']}",
                                        key=f"img_{page_num}_{idx}"
                                    )
                else:
                    st.warning("Δεν βρέθηκαν εικόνες στο PDF")
    
    st.markdown("---")
    
    # ΣΗΜΕΙΩΣΕΙΣ ΧΡΗΣΤΗ
    st.subheader("📝 Σημειώσεις")
    notes = st.text_area("Οι σημειώσεις σας:", height=200, label_visibility="collapsed")

with col1:
#   if selected_file:

        file_path = os.path.join(folder_path, selected_file)
        
        # ΡΥΘΜΙΣΕΙΣ ZOOM
        st.subheader("📄 Προβολή PDF")
        
        zoom_col1, zoom_col2 = st.columns(2)
        with zoom_col1:
            zoom_level = st.slider("Εστιασμός (zoom)", 0.5, 3.0, 1.0, 0.1)
        with zoom_col2:
            page_height = st.selectbox("Ύψος προβολής", ["600px", "800px", "1000px", "1200px"], index=1)
        
        # Εμφάνιση PDF με zoom
        try:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            
            # CSS για zoom
            zoom_css = f"""
            <style>
            .pdf-viewer {{
                transform: scale({zoom_level});
                transform-origin: 0 0;
                width: {100/zoom_level}%;
                height: {100/zoom_level}%;
            }}
            </style>
            """
            
            st.markdown(zoom_css, unsafe_allow_html=True)
            
            st.markdown(
                f'<div style="overflow: auto; height: {page_height}; border: 1px solid #ddd; padding: 10px;">'
                f'<div class="pdf-viewer">'
                f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
                f'width="100%" height="100%" type="application/pdf" '
                f'style="border: none;"></iframe>'
                f'</div></div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Σφάλμα φόρτωσης PDF: {e}")
        
        # ΚΕΙΜΕΝΟ ΑΝΑ ΣΕΛΙΔΑ (ΜΕ SELECTBOX)
        st.markdown("---")
        st.subheader("📖 Κείμενο ανά Σελίδα")
        
        # Αριθμός σελίδων
        try:
            doc = fitz.open(file_path)
            total_pages = len(doc)
            doc.close()
            
            if total_pages > 0:
                # Selectbox για επιλογή σελίδας
                page_options = [f"Σελίδα {i+1}" for i in range(total_pages)]
                selected_page_label = st.selectbox(
                    "Επιλέξτε σελίδα:",
                    page_options,
                    index=0
                )
                
                # Εξαγωγή αριθμού σελίδας
                selected_page_num = int(selected_page_label.split()[-1]) - 1
                
                # Εμφάνιση κειμένου επιλεγμένης σελίδας
                doc = fitz.open(file_path)
                page = doc[selected_page_num]
                page_text = page.get_text()
                doc.close()
                
                if page_text.strip():
                    st.text_area(
                        f"Κείμενο {selected_page_label}",
                        page_text,
                        height=300,
                        key=f"page_{selected_page_num}"
                    )
                    
                    # Κουμπί λήψης για συγκεκριμένη σελίδα
                    st.download_button(
                        label=f"📥 Λήψη κειμένου {selected_page_label}",
                        data=page_text,
                        file_name=f"{os.path.splitext(selected_file)[0]}_page_{selected_page_num+1}.txt",
                        mime="text/plain",
                        key=f"download_page_{selected_page_num}"
                    )
                else:
                    st.info("Αυτή η σελίδα δεν περιέχει κείμενο")
            else:
                st.warning("Το PDF δεν έχει σελίδες")
                
        except Exception as e:
            st.error(f"Σφάλμα ανάγνωσης σελίδων: {e}")
        
        # ΠΛΗΡΕΣ ΚΕΙΜΕΝΟ (ΟΠΤΙΚΑ)
        st.markdown("---")
        with st.expander("📄 Πλήρες κείμενο PDF (όλες οι σελίδες)"):
            if st.button("Εξαγωγή πλήρους κειμένου"):
                with st.spinner("Εξαγωγή κειμένου..."):
                    full_text = pdf_open_streamlit(file_path)
                    
                    if full_text:
                        st.text_area("Πλήρες κείμενο", full_text, height=400)
                        
                        st.download_button(
                            label="📥 Λήψη πλήρους κειμένου",
                            data=full_text,
                            file_name=f"{os.path.splitext(selected_file)[0]}_full.txt",
                            mime="text/plain",
                            key="download_full"
                        )
                    else:
                        st.warning("Δεν βρέθηκε κείμενο στο PDF")

if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        
        st.subheader("📄 Προβολή PDF (Υψηλής Ποιότητας)")
        
        # Δημιουργία προσωρινού αρχείου για καλύτερη απόδοση
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            with open(file_path, 'rb') as f:
                tmp_file.write(f.read())
            tmp_path = tmp_file.name
        
        try:
            # Χρήση pdf_viewer component
            pdf_viewer(
                tmp_path,
                width=700,
                height=800,
                pages_to_render=[1, 2, 3, 4, 5],  # Πρώτες 5 σελίδες
                rendering="canvas",  # "canvas" για καλύτερη ποιότητα
            
            )
        finally:
            # Καθαρισμός προσωρινού αρχείου
            os.unlink(tmp_path)


