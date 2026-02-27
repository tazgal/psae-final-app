from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from mistralai import Mistral
from dotenv import load_dotenv
import os

# 1. Φόρτωσε τα tokens από το .env
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# 2. Φόρτωσε το μοντέλο για embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Λίστα με τις ειδήσεις
news_texts = [
    "Ο πρωθυπουργός μίλησε στο σεμινάριο για την ενέργεια",
    "Η αντιπολίτευση καταδίκασε την ενέργεια αυτή",
    "Ο Τραμπ συνάντησε τον Σί"
]

# 4. Δημιουργία embeddings
embeddings = model.encode(news_texts)

# 5. Δημιουργία βάσης FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# 6. Αποθήκευση βάσης (προαιρετικά)
faiss.write_index(index, "news_index.faiss")

# 7. Ερώτημα
query = "Τι έκανε ο Τραμπ;"
query_embedding = model.encode([query])

# 8. Αναζήτηση σχετικών ειδήσεων
k = 3
distances, indices = index.search(query_embedding, k)
relevant_news = [news_texts[i] for i in indices[0]]

print(f"Σχετικές ειδήσεις: {relevant_news}")

# 9. Αρχικοποίηση του Mistral client
client = Mistral(api_key=mistral_api_key)

# 10. Αποστολή ερώτηματος στο Mistral
try:
    response = client.chat.complete(  
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": f"""
                Χρησιμοποίησε τις ακόλουθες ειδήσεις για να απαντήσεις στο ερώτημα:
                Ειδήσεις: {relevant_news}
                Ερώτημα: {query}
                Απάντηση:
                """
            }
        ]
    )
    # 11. Εκτύπωσε την απάντηση
    print("Απάντηση από Mistral:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Σφάλμα κατά την κλήση του Mistral API: {e}")