# το κομμάτι αυτό σώζει μόνο τα embeddings - ενώ στο άλλο μισό είναι αυτό για τα queries

import sqlite3
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "news_05.db"
INDEX_PATH = "news_index.faiss"
IDS_PATH = "news_ids.npy"
TEXTS_PATH = "news_texts.npy"

def create_and_save_embeddings():
    """Δημιουργεί και αποθηκεύει τα embeddings μία φορά"""
    
    # Φόρτωση δεδομένων από βάση
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT id, title, text FROM news_table")
    rows = cur.fetchall()
    conn.close()
    
    print(f"📦 Φόρτωση {len(rows)} εγγραφών από τη βάση")
    
    # Προεπεξεργασία κειμένων
    texts = []
    ids = []
    for row in rows:
        combined = f"{row['title'] or ''}: {row['text'] or ''}"[:1000]
        texts.append(combined)
        ids.append(row['id'])
    
    # Δημιουργία embeddings
    print("🎯 Δημιουργία embeddings...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
    embeddings = embeddings.astype("float32")
    
    # Δημιουργία και αποθήκευση FAISS index
    print("💾 Αποθήκευση FAISS index...")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    faiss.normalize_L2(embeddings)  # Κανονικοποίηση για cosine similarity
    index.add(embeddings)
    
    faiss.write_index(index, INDEX_PATH)
    np.save(IDS_PATH, np.array(ids))
    np.save(TEXTS_PATH, np.array(texts, dtype=object))
    
    print(f"✅ Αποθηκεύτηκαν: {len(ids)} εγγραφές")
    print(f"📊 Διαστάσεις embeddings: {embeddings.shape}")

if __name__ == "__main__":
    create_and_save_embeddings()