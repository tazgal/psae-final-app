from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from mistralai import Mistral
from dotenv import load_dotenv
import os

# 1. Φόρτωση API key
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# 2. Μοντέλο για embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Ορισμός διαδρομών
index_path = "news_index.faiss"
texts_path = "news_texts.npy"

# 4. Φόρτωση ή δημιουργία FAISS index
if os.path.exists(index_path) and os.path.exists(texts_path):
    print("✅ Φόρτωση υπάρχουσας βάσης FAISS...")
    index = faiss.read_index(index_path)
    news_texts = np.load(texts_path, allow_pickle=True).tolist()
    print(f"📊 Βάση περιέχει {len(news_texts)} ειδήσεις")
else:
    print("🆕 Δημιουργία νέας βάσης FAISS...")
    index = None
    news_texts = []

# 5. Συνάρτηση για προσθήκη νέας είδησης
def add_news(new_text):
    global index, news_texts
    
    # Δημιουργία embedding με κανονικοποίηση
    embedding = model.encode([new_text], normalize_embeddings=True)
    
    if index is None:
        # ΧΡΗΣΗ IndexFlatIP (Inner Product) για cosine similarity
        index = faiss.IndexFlatIP(embedding.shape[1])
        print(f"🆕 Δημιουργία νέου FAISS index με {embedding.shape[1]} διαστάσεις")
    
    index.add(embedding.astype("float32"))
    news_texts.append(new_text)
    
    # Αποθήκευση ενημερωμένων δεδομένων
    faiss.write_index(index, index_path)
    np.save(texts_path, np.array(news_texts, dtype=object))
    print(f"📰 Προστέθηκε: {new_text[:50]}...")

# 6. Προσθήκη ειδήσεων
eidiseis = [
    "Στα Βορίζια έγινε μακελειό", 
    "Ο Τραμπ κάνει τον καμπόσο", 
    "Συνάντηση Τραμπ Σι"
]

print("📥 Προσθήκη ειδήσεων...")
for item in eidiseis:
    add_news(item)

print(f"\n📊 Συνολικά {len(news_texts)} ειδήσεις στη βάση")

# 7. Ερώτημα
query = "Τι έγινε στα Βορίζια;"
print(f"\n🔍 Αναζήτηση: '{query}'")

# Query embedding με την ΙΔΙΑ κανονικοποίηση
query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")

k = min(5, len(news_texts))  # Ασφαλής τιμή για k

# Αναζήτηση
distances, indices = index.search(query_embedding, k)

print(f"📈 Αποτελέσματα αναζήτησης:")
print(f"   Indices: {indices}")
print(f"   Distances: {distances}")

# Ασφαλής ανάκτηση αποτελεσμάτων
relevant_news = []
for i in indices[0]:
    if i != -1 and 0 <= i < len(news_texts):  # Έλεγχος για έγκυρα indices
        relevant_news.append(news_texts[i])

print(f"\n📰 Βρέθηκαν {len(relevant_news)} σχετικές ειδήσεις:")
for i, news in enumerate(relevant_news, 1):
    print(f"{i}. {news}")

# 8. Κλήση Mistral API
if relevant_news and mistral_api_key:
    client = Mistral(api_key=mistral_api_key)

    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Χρησιμοποίησε τις ακόλουθες πληροφορίες για να απαντήσεις:

                    Πληροφορίες:
                    {chr(10).join([f'- {news}' for news in relevant_news])}

                    Ερώτημα: {query}

                    Απάντησε στα Ελληνικά:
                    """
                }
            ]
        )
        
        print("\n" + "="*50)
        print("🤖 ΑΠΑΝΤΗΣΗ MISTRAL:")
        print("="*50)
        print(response.choices[0].message.content)
        print("="*50)
        
    except Exception as e:
        print(f"⚠️ Σφάλμα κατά την κλήση του Mistral API: {e}")
else:
    print("❌ Δεν υπάρχουν σχετικές ειδήσεις ή λείπει το API key")