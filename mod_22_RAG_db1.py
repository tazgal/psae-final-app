import sqlite3
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from mistralai import Mistral
from dotenv import load_dotenv
import gc
import psutil
import logging

# Ρύθμιση logging για παρακολούθηση μνήμης
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_memory_usage():
    """Παρακολούθηση χρήσης μνήμης"""
    process = psutil.Process(os.getpid())
    return f"{process.memory_info().rss / 1024 / 1024:.2f} MB"

# -----------------------------------
# 1️⃣ Φόρτωση Mistral API key
# -----------------------------------
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

if not mistral_api_key:
    raise ValueError("❌ Δεν βρέθηκε MISTRAL_API_KEY στο .env αρχείο!")

# -----------------------------------
# 2️⃣ Βελτιστοποιημένη σύνδεση με SQLite
# -----------------------------------
def load_data_in_batches(db_path, batch_size=1000):
    """Φόρτωση δεδομένων από τη βάση σε batches"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Για πιο αποδοτική πρόσβαση
    
    try:
        cur = conn.cursor()
        
        # Πρώτα μετρήσουμε το σύνολο των εγγραφών
        cur.execute("SELECT COUNT(*) as count FROM news_table")
        total_rows = cur.fetchone()['count']
        logger.info(f"📦 Βρέθηκαν {total_rows} εγγραφές στη βάση")
        
        # Φόρτωση δεδομένων σε batches
        offset = 0
        all_rows = []
        all_ids = []
        
        while offset < total_rows:
            cur.execute(
                "SELECT id, title, text FROM news_table LIMIT ? OFFSET ?", 
                (batch_size, offset)
            )
            batch_rows = cur.fetchall()
            
            if not batch_rows:
                break
                
            all_rows.extend(batch_rows)
            all_ids.extend([row['id'] for row in batch_rows])
            
            logger.info(f"📥 Φόρτωση batch {offset//batch_size + 1}: {len(batch_rows)} εγγραφές - Μνήμη: {get_memory_usage()}")
            
            offset += batch_size
            
            # Καθαρισμός μνήμης μεταξύ batches
            if offset % 5000 == 0:
                gc.collect()
                
        return all_rows, all_ids
        
    finally:
        conn.close()

# -----------------------------------
# 3️⃣ Βελτιστοποιημένη δημιουργία embeddings
# -----------------------------------
def create_embeddings_optimized(model, texts, batch_size=64):
    """Δημιουργία embeddings με βελτιστοποιημένη διαχείριση μνήμης"""
    logger.info(f"🎯 Δημιουργία embeddings για {len(texts)} κείμενα...")
    
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        
        # Δημιουργία embeddings για το τρέχον batch
        batch_embeddings = model.encode(
            batch_texts, 
            batch_size=32,  # Μικρότερο batch size για encoding
            show_progress_bar=False,  # Απενεργοποίηση progress bar για μείωση memory overhead
            convert_to_numpy=True,
            normalize_embeddings=True  # Κανονικοποίηση για καλύτερη απόδοση FAISS
        )
        
        all_embeddings.append(batch_embeddings)
        
        # Καθαρισμός μνήμης
        del batch_embeddings
        if (i // batch_size) % 10 == 0:
            gc.collect()
            
        logger.info(f"✅ Ολοκληρώθηκε batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1} - Μνήμη: {get_memory_usage()}")
    
    # Συνένωση όλων των embeddings
    final_embeddings = np.vstack(all_embeddings).astype("float32")
    
    return final_embeddings

# -----------------------------------
# 4️⃣ Βελτιστοποιημένη διαχείριση FAISS index
# -----------------------------------
def setup_faiss_index(embeddings, ids, index_path="news_index.faiss", ids_path="news_ids.npy"):
    """Δημιουργία ή φόρτωση FAISS index με βελτιστοποιήσεις"""
    
    if os.path.exists(index_path) and os.path.exists(ids_path):
        logger.info("✅ Φόρτωση υπάρχοντος FAISS index...")
        
        # Χρήση memory-mapped index για μεγάλα datasets
        index = faiss.read_index(index_path)
        stored_ids = np.load(ids_path)
        
        return index, stored_ids
    else:
        logger.info("🆕 Δημιουργία νέου FAISS index...")
        
        # Χρήση IndexFlatIP με κανονικοποιημένα embeddings για cosine similarity
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner Product για cosine similarity
        
        # Προσθήκη embeddings (είναι ήδη normalized από το normalize_embeddings=True)
        index.add(embeddings)
        
        # Αποθήκευση
        faiss.write_index(index, index_path)
        np.save(ids_path, np.array(ids))
        
        logger.info("💾 Ο index αποθηκεύτηκε για μελλοντική χρήση.")
        
        return index, np.array(ids)

# -----------------------------------
# ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ
# -----------------------------------
def main():
    try:
        logger.info("🚀 Εκκίνηση εφαρμογής...")
        
        # Παράμετροι βελτιστοποίησης
        DB_PATH = "news_05.db"
        BATCH_SIZE_DATA = 2000  # Batch size για φόρτωση από βάση
        BATCH_SIZE_EMBEDDINGS = 128  # Batch size για δημιουργία embeddings
        
        # -----------------------------------
        # Φόρτωση δεδομένων
        # -----------------------------------
        logger.info("📥 Φόρτωση δεδομένων από βάση...")
        rows, ids = load_data_in_batches(DB_PATH, BATCH_SIZE_DATA)
        
        if not rows:
            logger.error("❌ Δεν βρέθηκαν δεδομένα στη βάση!")
            return
        
        # -----------------------------------
        # Προεπεξεργασία κειμένων
        # -----------------------------------
        logger.info("🔧 Προεπεξεργασία κειμένων...")
        texts = []
        for row in rows:
            title = row['title'] or ""
            text = row['text'] or ""
            # Συνδυασμός title + text με περιορισμό μήκους
            combined = f"{title}: {text}"[:1000]  # Περιορισμός μήκους για μείωση memory
            texts.append(combined)
        
        # Απελευθέρωση μνήμης
        del rows
        gc.collect()
        
        # -----------------------------------
        # Φόρτωση μοντέλου και δημιουργία embeddings
        # -----------------------------------
        logger.info("🤖 Φόρτωση μοντέλου embeddings...")
        
        # Χρήση μικρότερου μοντέλου για μείωση memory footprint
        model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 διαστάσεις αντί για 768
        
        embeddings = create_embeddings_optimized(model, texts, BATCH_SIZE_EMBEDDINGS)
        
        # Απελευθέρωση μνήμης από το μοντέλο μετά τη χρήση
        del model
        gc.collect()
        
        logger.info(f"📊 Δημιουργήθηκαν embeddings: {embeddings.shape} - Μνήμη: {get_memory_usage()}")
        
        # -----------------------------------
        # Ρύθμιση FAISS
        # -----------------------------------
        index, stored_ids = setup_faiss_index(embeddings, ids)
        
        # Απελευθέρωση μνήμης από embeddings μετά τη δημιουργία index
        del embeddings
        gc.collect()
        
        # -----------------------------------
        # Αναζήτηση
        # -----------------------------------
        query = input("🔍 Δώσε ερώτημα: ").strip()
        
        if not query:
            logger.info("❌ Δεν δόθηκε ερώτημα!")
            return
        
        # Φόρτωση μοντέλου για query (ξανά, αφού το διαγράψαμε νωρίτερα)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")
        del model
        
        k = min(5, len(stored_ids))  # Ασφαλής τιμή για k
        distances, indices = index.search(query_embedding, k)
        
        relevant_ids = [int(stored_ids[i]) for i in indices[0] if i < len(stored_ids)]
        
        if not relevant_ids:
            logger.info("❌ Δεν βρέθηκαν σχετικά αποτελέσματα!")
            return
        
        # -----------------------------------
        # Ανάκτηση πληροφοριών από βάση
        # -----------------------------------
        conn = sqlite3.connect(DB_PATH)
        try:
            placeholders = ','.join('?' * len(relevant_ids))
            cur = conn.cursor()
            cur.execute(
                f"SELECT title, text FROM news_table WHERE id IN ({placeholders})",
                relevant_ids
            )
            context_rows = cur.fetchall()
            
            # Δημιουργία context με περιορισμό μήκους
            context_parts = []
            for title, text in context_rows:
                # Περιορισμός μήκους κάθε άρθρου
                truncated_text = text[:800] + "..." if len(text) > 800 else text
                context_parts.append(f"Τίτλος: {title}\nΚείμενο: {truncated_text}")
            
            context = "\n\n".join(context_parts)
            
            print(f"\n📰 Βρέθηκαν {len(context_rows)} σχετικά άρθρα:")
            for i, (title, _) in enumerate(context_rows, 1):
                print(f"{i}. {title}")
                
        finally:
            conn.close()
        
        # -----------------------------------
        # Κλήση Mistral API
        # -----------------------------------
        logger.info("🤖 Κλήση Mistral API...")
        
        client = Mistral(api_key=mistral_api_key)
        
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": f"""Βασίσου ΑΠΟΚΛΕΙΣΤΙΚΑ στις παρακάτω πηγές:

Πηγές:
{context}

Ερώτηση: {query}

Απάντησε στα Ελληνικά με βάση τις πηγές και μην αναφέρεις πληροφορίες από αλλού."""
                }
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        print("\n" + "="*50)
        print("🤖 ΑΠΑΝΤΗΣΗ:")
        print("="*50)
        print(response.choices[0].message.content)
        print("="*50)
        
    except Exception as e:
        logger.error(f"❌ Σφάλμα: {e}")
        raise

if __name__ == "__main__":
    main()