import streamlit as st
import os
import faiss
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from mistralai import Mistral
from dotenv import load_dotenv
import tempfile

# --- Ρυθμίσεις ---
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    st.error("❌ Δεν υπάρχει MISTRAL_API_KEY στο .env αρχείο!")
    st.stop()

EMB_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# --- Μοντέλα ---
@st.cache_resource
def load_models():
    model = SentenceTransformer(EMB_MODEL)
    client = Mistral(api_key=MISTRAL_API_KEY)
    return model, client

model, client = load_models()

# --- 1️⃣ Εξαγωγή κειμένου από PDF ---
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# --- 2️⃣ Τεμαχισμός σε chunks ---
def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# --- 3️⃣ Δημιουργία FAISS index ---
def build_faiss_index(chunks, model):
    # 🧩 Safety checks
    if not chunks:
        raise ValueError("❌ Δεν βρέθηκαν κομμάτια κειμένου. Έλεγξε αν το PDF περιέχει αναγνώσιμο κείμενο.")

    # Ensure chunks is always a list of strings
    if isinstance(chunks, str):
        chunks = [chunks]

    # Encode
    embeddings = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)

    # Convert list to numpy if needed
    if isinstance(embeddings, list):
        embeddings = np.array(embeddings, dtype=np.float32)

    # Ensure 2D shape (e.g. (N, 384))
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype(np.float32))

    # Optional debugging info
    st.write(f"📏 Embeddings shape: {embeddings.shape}")

    return index, embeddings


# --- 4️⃣ RAG Query ---
def query_rag(index, chunks, query, model, client, top_k=3):
    q_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
    D, I = index.search(q_emb, top_k)
    retrieved = [chunks[i] for i in I[0]]
    context = "\n\n".join(retrieved)

    prompt = f"""Βασίσου αποκλειστικά στις παρακάτω πληροφορίες:

{context}

Ερώτηση: {query}
Απάντησε στα ελληνικά:"""

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

# --- UI ---
st.set_page_config(page_title="📄 PDF RAG με Mistral", page_icon="🤖")
st.title("📄 PDF RAG Chatbot με Mistral")
st.write("Ανέβασε ένα PDF και κάνε ερωτήσεις πάνω στο περιεχόμενό του!")

uploaded_file = st.file_uploader("📤 Ανέβασε PDF", type="pdf")

def pdf_to_rag_streamlit(uploaded_file):

    if uploaded_file:
        with st.spinner("📖 Εξαγωγή κειμένου από PDF..."):
            text = extract_text_from_pdf(uploaded_file)
            chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            index, _ = build_faiss_index(chunks, model)
        st.success(f"✅ Επεξεργάστηκαν {len(chunks)} κομμάτια κειμένου!")

        query = st.text_input("💬 Κάνε μια ερώτηση πάνω στο PDF:")
        if query:
            with st.spinner("🤖 Δημιουργία απάντησης από Mistral..."):
                answer = query_rag(index, chunks, query, model, client)
            st.markdown("### 🧠 Απάντηση:")
            st.write(answer)
    else:
        st.info("⬆️ Ανέβασε ένα PDF για να ξεκινήσεις.")
