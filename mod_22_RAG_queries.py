# query_only.py
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from mistralai import Mistral
from dotenv import load_dotenv
import os

# ==============================
# ΡΥΘΜΙΣΕΙΣ
# ==============================
DEBUG = True
INDEX_PATH = "news_index.faiss"
IDS_PATH = "news_ids.npy"
TEXTS_PATH = "news_texts.npy"

# ==============================
# Φόρτωση API Key
# ==============================
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    raise ValueError("❌ Δεν βρέθηκε MISTRAL_API_KEY!")

# ==============================
# Φόρτωση ΠREEXISTING Βάσης
# ==============================
def load_precomputed_data():
    """Φορτώνει το προϋπολογισμένο index και τα δεδομένα"""
    if not all(os.path.exists(path) for path in [INDEX_PATH, IDS_PATH, TEXTS_PATH]):
        raise FileNotFoundError("❌ Τα αρχεία βάσης δεν βρέθηκαν. Τρέχε πρώτα το save_embeddings.py")
    
    print("📂 Φόρτωση προϋπολογισμένων δεδομένων...")
    index = faiss.read_index(INDEX_PATH)
    ids = np.load(IDS_PATH)
    texts = np.load(TEXTS_PATH, allow_pickle=True)
    
    print(f"✅ Φορτώθηκε index με {index.ntotal} εγγραφές")
    return index, ids, texts

# ==============================
# ΑΝΑΖΗΤΗΣΗ ΚΑΙ ΑΠΑΝΤΗΣΗ
# ==============================
def search_and_answer(query, index, ids, texts, k=5):
    """Αναζήτηση και απάντηση για συγκεκριμένο ερώτημα"""
    
    # Φόρτωση μοντέλου για embedding του query
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    
    # Δημιουργία embedding για το query
    query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")
    
    # Αναζήτηση στο FAISS
    distances, indices = index.search(query_embedding, k)
    
    # Ανάκτηση σχετικών εγγραφών
    relevant_indices = [i for i in indices[0] if 0 <= i < len(texts)]
    relevant_texts = [texts[i] for i in relevant_indices]
    relevant_ids = [ids[i] for i in relevant_indices]
    
    if DEBUG:
        print(f"🔍 Αποτελέσματα για '{query}':")
        print(f"📊 Βρέθηκαν {len(relevant_texts)} σχετικά κείμενα")
        for i, (text, score) in enumerate(zip(relevant_texts, distances[0][:len(relevant_texts)])):
            print(f"{i+1}. Score: {score:.4f}")
            print(f"   Text: {text[:100]}...")
            print()
    
    return relevant_texts

def get_mistral_response(query, context_texts):
    """Απάντηση από το Mistral API"""
    
    client = Mistral(api_key=mistral_api_key)
    
    # Δημιουργία context
    context = "\n\n".join([f"[Πηγή {i+1}]: {text}" for i, text in enumerate(context_texts)])
    
    if DEBUG:
        print("🧾 Πληροφορίες που στέλνονται στο Mistral:")
        print(context[:1500] + "..." if len(context) > 1500 else context)
        print("=" * 50)
    
    # Κλήση API
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{
            "role": "user",
            "content": f"""Βασίσου ΑΠΟΚΛΕΙΣΤΙΚΑ στις παρακάτω πηγές:

Πηγές:
{context}

Ερώτηση: {query}

Απάντησε στα Ελληνικά με βάση τις πηγές. Αν οι πηγές δεν περιέχουν αρκετές πληροφορίες, πες απλώς ότι δεν υπάρχουν αρκετές πληροφορίες διαθέσιμες."""
        }],
        max_tokens=800,
        temperature=0.3
    )
    
    return response.choices[0].message.content

# ==============================
# ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ ΕΡΩΤΗΣΕΩΝ
# ==============================
def main():
    # Φόρτωση προϋπολογισμένων δεδομένων (ΓΙΝΕΤΑΙ ΜΟΝΟ ΜΙΑ ΦΟΡΑ)
    index, ids, texts = load_precomputed_data()
    
    print("\n" + "="*60)
    print("🤖 ΣΥΣΤΗΜΑ ΕΡΩΤΗΣΕΩΝ - Έτοιμο!")
    print("="*60)
    
    while True:
        print("\n" + "-"*40)
        query = input("🔍 Δώσε ερώτημα (ή 'exit' για έξοδο): ").strip()
        
        if query.lower() in ['exit', 'έξοδος', 'quit']:
            print("👋 Έξοδος...")
            break
            
        if not query:
            print("⚠️ Παρακαλώ δώσε ένα ερώτημα.")
            continue
        
        try:
            # Αναζήτηση
            relevant_texts = search_and_answer(query, index, ids, texts)
            
            if not relevant_texts:
                print("❌ Δεν βρέθηκαν σχετικά αποτελέσματα.")
                continue
            
            # Απάντηση από Mistral
            print("\n🎯 ΑΝΑΖΗΤΗΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ - Καλείται Mistral API...")
            answer = get_mistral_response(query, relevant_texts)
            
            print("\n" + "="*50)
            print("🤖 ΑΠΑΝΤΗΣΗ:")
            print("="*50)
            print(answer)
            print("="*50)
            
        except Exception as e:
            print(f"❌ Σφάλμα: {e}")

if __name__ == "__main__":
    main()