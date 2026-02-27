import os
import requests
from dotenv import load_dotenv
import streamlit as st
import re
from mistralai import Mistral
from dotenv import load_dotenv


def gpt_mistral_diorthosi_streamlit(text):
    api_key = st.secrets.get("MISTRAL_API_KEY")
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "system",
            "content": "Είσαι ένας βοηθός που κάνει μόνο ορθογραφική διόρθωση στα ελληνικά. "
                       "Βάζεις τόνους, διορθώνεις ορθογραφικά λάθη, αλλά δεν αλλάζεις τη διατύπωση."
            },
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)

st.header("NewsRoom Tools")
        
user_text = st.text_area("Βάλε το κείμενο εδώ:", height=200)

if st.button("Διόρθωσε το κείμενο"):
    gpt_mistral_diorthosi_streamlit(user_text)
