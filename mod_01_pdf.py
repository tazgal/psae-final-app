import fitz  # PyMuPDF
import streamlit as st
from natural_pdf import PDF
import os
import base64
import fitz



def pdf_open_streamlit(pdf):

    doc = fitz.open(pdf)
    text = ""
    for page in doc:
        text += page.get_text()

    if pdf is not None:
        st.write("Το αρχείο ανέβηκε με επιτυχία")

        st.subheader("Το κείμενο")
        st.write(text)

        st.download_button(
            label="Αποθήκευσε το κείμενο σε txt",
            data=text,
            file_name="κειμενο_απο_pdf.txt",
            mime="text/plain")


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
    
    
    pdf = PDF(pdf_path)
    for i, page in enumerate(pdf.pages):
        page_tables = page.extract_tables()
        if page_tables:
            for table in page_tables:
                tables.append({
                    "page": i + 1,
                    "table": table
                })

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