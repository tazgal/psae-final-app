import requests
import streamlit as st

API_URL1 = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-mul-en"
API_URL2 = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-en-el"
headers = {
    "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
}
"""
def query_en(payload):
    response = requests.post(API_URL1, headers=headers, json=payload)
    return response.json()

def query_el(payload):
    response = requests.post(API_URL2, headers=headers, json=payload)
    return response.json()

x = input("Δώσε κείμενο: ").strip()

output = query_el({"inputs": x})
print(output)
"""

def translate_hels_el(text):
    payload = {"inputs": text}
    response = requests.post(API_URL2, headers=headers, json=payload)
    return response.json()  # επιστρέφει το JSON

def translate_el_streamlit():
    x = input("Δώσε κείμενο: ").strip()
    output = translate_hels_el(x)
    translated_text = output[0]['translation_text']
    st.write(translated_text)

def translate_el_streamlit2(text):
    output = translate_hels_el(text)
    translated_text = output[0]['translation_text']
    st.write(translated_text)