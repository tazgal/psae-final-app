import pytesseract
from PIL import Image
import streamlit as st


def ocr_reader():
    text = pytesseract.image_to_string(
        Image.open("testphoto2.jpg"),
        lang="ell"   # κωδικός για ελληνικά
    )

    print(text)


def ocr_reader_streamlit(uploaded_photo):
    # uploaded_photo είναι ήδη αρχείο-αντικείμενο (BytesIO)
    img = Image.open(uploaded_photo)
    text = pytesseract.image_to_string(img, lang="ell")  # ελληνικά
    st.write(text)


