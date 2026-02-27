import base64
import os
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from PIL import Image
import io

# =========================
# ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ
# =========================

def extract_images_from_pdf(pdf_path):
    images = []
    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base = doc.extract_image(xref)
            images.append({
                "page": page_num + 1,
                "index": img_index + 1,
                "bytes": base["image"],
                "ext": base["ext"]
            })

    doc.close()
    return images


def extract_text_all_pages(pdf_path):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    return text


# =========================
# STREAMLIT APP
# =========================

st.set_page_config(layout="wide")
st.title("📄 PDF Viewer & Extractor")

folder_path = "data/economy_files/economy_pdfs"

col1, col2 = st.columns([4, 1], gap="medium")

# =========================
# ΔΕΞΙΑ ΣΤΗΛΗ – ΕΠΙΛΟΓΕΣ
# =========================

with col2:
    st.subheader("📂 Επιλογή PDF")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    selected_file = st.selectbox("Αρχείο PDF", files) if files else None

    st.markdown("---")

    st.subheader("📝 Σημειώσεις")
    st.text_area("Notes", height=200, label_visibility="collapsed")

# =========================
# ΑΡΙΣΤΕΡΗ ΣΤΗΛΗ – ΠΡΟΒΟΛΗ
# =========================

with col1:
    if selected_file:
        file_path = os.path.join(folder_path, selected_file)

        # -------- ΡΥΘΜΙΣΕΙΣ --------
        st.subheader("📄 Προβολή PDF")

        z1, z2 = st.columns(2)
        zoom = z1.slider("Zoom", 0.5, 2.5, 1.0, 0.1)
        height = z2.selectbox("Ύψος Viewer", ["700px", "900px", "1100px"], index=1)

        # -------- PDF VIEWER --------
        with open(file_path, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <style>
            .pdf-wrap {{
                transform: scale({zoom});
                transform-origin: 0 0;
                width: {100/zoom}%;
            }}
            </style>

            <div style="height:{height}; overflow:auto; border:1px solid #ccc;">
                <div class="pdf-wrap">
                    <iframe src="data:application/pdf;base64,{pdf_base64}"
                            width="100%" height="100%" style="border:none;"></iframe>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------- ΚΕΙΜΕΝΟ ΑΝΑ ΣΕΛΙΔΑ --------
        st.markdown("---")
        st.subheader("📖 Κείμενο ανά Σελίδα")

        doc = fitz.open(file_path)
        total_pages = len(doc)
        page_num = st.selectbox("Σελίδα", range(1, total_pages + 1))
        page_text = doc[page_num - 1].get_text()
        doc.close()

        st.text_area(
            f"Σελίδα {page_num}",
            page_text if page_text.strip() else "— Δεν υπάρχει κείμενο —",
            height=300
        )

        st.download_button(
            "📥 Λήψη κειμένου σελίδας",
            page_text,
            file_name=f"{selected_file}_page_{page_num}.txt"
        )

        # -------- ΠΛΗΡΕΣ ΚΕΙΜΕΝΟ --------
        st.markdown("---")
        with st.expander("📄 Πλήρες κείμενο PDF"):
            if st.button("Εξαγωγή πλήρους κειμένου"):
                full_text = extract_text_all_pages(file_path)
                st.text_area("Όλο το κείμενο", full_text, height=400)

        # -------- ΕΙΚΟΝΕΣ --------
        st.markdown("---")
        st.subheader("🖼️ Εικόνες PDF")

        images = extract_images_from_pdf(file_path)

        if images:
            for img in images:
                st.image(
                    img["bytes"],
                    caption=f"Σελίδα {img['page']} – Εικόνα {img['index']}"
                )
                st.download_button(
                    "📥 Λήψη εικόνας",
                    img["bytes"],
                    file_name=f"page_{img['page']}_img_{img['index']}.{img['ext']}"
                )
        else:
            st.info("Δεν βρέθηκαν εικόνες")

    else:
        st.info("⬅️ Επέλεξε ένα PDF από δεξιά")
