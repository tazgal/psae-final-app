import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# 1. Δημιουργία client και collection
client = chromadb.PersistentClient(path="chroma_db")
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
collection = client.create_collection(
    name="news",
    embedding_function=embedding_function
)

# 2. Προσθήκη εγγραφών
records = [
    {"content": "Υπό αστυνομικό κλοιό το χωριό Βορίζια...", "metadata": {"source": "eurokinissi"}},
    {"content": "Ο Κασιδιάρης απολογήθηκε στη δίκη...", "metadata": {"source": "ta nea"}}
]
collection.add(
    documents=[record["content"] for record in records],
    metadatas=[record["metadata"] for record in records],
    ids=[f"id{i}" for i in range(len(records))]
)

# 3. Αναζήτηση
results = collection.query(
    query_texts=["Τι έγινε στα Βορίζια;"],
    n_results=3
)
print(results)
