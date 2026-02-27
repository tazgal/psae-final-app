# ********************* ΒΙΒΛΙΟΘΗΚΕΣ *********************

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)
from mod_05_sql import sq_choose_txt_column_spec_lines
import streamlit as st

# ********************* ΒΟΗΘΗΤΙΚΑ - ΣΗΜΕΙΩΣΕΙΣ *********************


# Μοντέλα που χρησιμοποιήθηκαν: https://huggingface.co/dascim/greekbart
# Pipeline για sentiment-analysis με DistilBERT
#ner = pipeline("ner", grouped_entities = True)
#text = "Despite near-term trade policy headwinds, Wall Street analysts are overwhelmingly bullish on the chipmaker’s prospects. Of the 13 analysts with current ratings surveyed by Visible Alpha, 12 call the stock a 'buy', compared to one 'hold' rating. Their targets range from $155 to $225, with the majority above $200, suggesting significant upside from Friday's close around $178."
#ner(text)

# ********************* DEFS *********************

def tr_generate_title(text):
    tokenizer = AutoTokenizer.from_pretrained("dascim/greekbart-news24-title")
    model = AutoModelForSeq2SeqLM.from_pretrained("dascim/greekbart-news24-title")

    input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')

    model.eval()
    predict = model.generate(input_ids, max_length=100)[0]

    x = tokenizer.decode(predict, skip_special_tokens=True)
    print(x)

def tr_generate_title_streamlit(text):
    tokenizer = AutoTokenizer.from_pretrained("dascim/greekbart-news24-title")
    model = AutoModelForSeq2SeqLM.from_pretrained("dascim/greekbart-news24-title")

    input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')

    model.eval()
    predict = model.generate(input_ids, max_length=100)[0]

    x = tokenizer.decode(predict, skip_special_tokens=True)
    st.write(x)

def tr_generate_summary(text):
    tokenizer = AutoTokenizer.from_pretrained("dascim/greekbart-news24-abstract")
    model = AutoModelForSeq2SeqLM.from_pretrained("dascim/greekbart-news24-abstract")

    input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')

    model.eval()
    predict = model.generate(input_ids, max_length=100)[0]

    x = tokenizer.decode(predict, skip_special_tokens=True)
    print(x)

def tr_generate_summary_streamlit(text):
    tokenizer = AutoTokenizer.from_pretrained("dascim/greekbart-news24-abstract")
    model = AutoModelForSeq2SeqLM.from_pretrained("dascim/greekbart-news24-abstract")

    input_ids = tokenizer.encode(text, add_special_tokens=True, return_tensors='pt')

    model.eval()
    predict = model.generate(input_ids, max_length=500)[0]

    x = tokenizer.decode(predict, skip_special_tokens=True)
    st.write(x)

#Παίρνει ειδήσεις από ΒΔ (ενδεικτικά, πρώτες σειρές) και βγάζει τίτλο και σύνοψη 
def tr_from_db_to_title_summary():
    texts = sq_choose_txt_column_spec_lines()
    for text in texts:
        text = str(text)
        tr_generate_title(text)
        tr_generate_summary(text)


# ********************* TEST AREA *********************
