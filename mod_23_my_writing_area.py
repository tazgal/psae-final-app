import streamlit as st
import pandas as pd
import json
from io import BytesIO, StringIO
import base64
import docx
from docx import Document
from PIL import Image
from streamlit_quill import st_quill
import os
from docx import Document
from html2docx import html2docx

from mod_01_enter_open import open_file_from_folder


st.set_page_config(
    page_title="Writing Area with Files",
    page_icon="",
    layout="wide"
)

def main_writing_area():
    
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.subheader("✍️ Writing Editor")
        
        content = st_quill(
            placeholder="Write here...",
            html=True,

        )

        folder = st.text_input(
            "Φάκελος αποθήκευσης",
            value="data/texts"
        )

        filename = st.text_input(
        "Όνομα αρχείου (χωρίς κατάληξη)",
        value="document"
        )

        file_format = st.selectbox(
            "Μορφή αρχείου",
            ["HTML", "DOCX"]
        )

        if st.button("Save content"):
            if not content:
                st.warning("⚠️ Δεν υπάρχει περιεχόμενο")
            else:
                os.makedirs(folder, exist_ok=True)

                # HTML
                if file_format == "HTML":
                    file_path = os.path.join(folder, f"{filename}.html")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

                # DOCX με ΠΛΗΡΕΣ formatting
                elif file_format == "DOCX":
                    file_path = os.path.join(folder, f"{filename}.docx")

                    # Λαμβάνουμε τα bytes από html2docx
                    doc_bytes = html2docx(content, title=filename)

                    # Αποθηκεύουμε τα bytes σε αρχείο
                    with open(file_path, "wb") as f:
                        f.write(doc_bytes.getvalue())


                st.success(f"✅ Αποθηκεύτηκε: {file_path}")

    with col2:
        
        st.text("βοηθητική περιοχή")

        open_file_from_folder("data/texts")


        


     

