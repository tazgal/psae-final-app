from transformers import pipeline
import streamlit as st


# Φορτώνουμε το QA μοντέλο μόνο μία φορά (cache)
@st.cache_resource

def load_model():
    return pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2")

qa_model = load_model()

st.title("🧠 Question Answering App")
st.write("Δώσε ένα κείμενο (context) και κάνε μια ερώτηση πάνω σε αυτό.")

# Πεδίο για το context
context = st.text_area("📜 Κείμενο (context)", 
    "My name is Tim and I live in Sweden.")

# Πεδίο για την ερώτηση
question = st.text_input("❓ Ερώτηση", "Where do I live?")

# Κουμπί εκτέλεσης
if st.button("Απάντησε"):
    if context and question:
        result = qa_model(question=question, context=context)
        st.subheader("📌 Απάντηση")
        st.write(result["answer"])

        st.caption(f"Confidence score: {result['score']:.2f}")
    else:
        st.warning("Δώσε και context και ερώτηση για να συνεχίσεις.")
