# Σε αυτό το mod υπάρχουν διάφορα εργαλεία για τη γλωσσική ανάλυση (τρίτο στάδιο) - πχ NER, NLP κοκ

# ********************* ΒΙΒΛΙΟΘΗΚΕΣ *********************

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.text import ConcordanceIndex
from nltk.corpus import stopwords
import spacy
from spacy.tokens import Span
import stanza
from mod_05_sql import sq_choose_txt_column_from_newstable_wtho_print, sq_choose_txt_column_spec_lines
from collections import defaultdict, Counter
from flair.models import SequenceTagger 
from flair.data import Sentence
from gensim.models import Word2Vec
from gensim import corpora, models
import dateparser
from dateparser.search import search_dates
import streamlit as st
import re
from spacy import displacy
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize


# ********************* ΒΟΗΘΗΤΙΚΑ *********************


# παίρνει από τον πίνακα νέα τη στήλη με τα κείμενα και την κάνει string (returns tokens)
def nltk_from_news_to_str():
    x = sq_choose_txt_column_from_newstable_wtho_print()  # λίστα από tuples
    texts = [row[0] for row in x]  # λίστα μόνο με τα strings
    text_string = " ".join(texts)  # ενώνεις τα κείμενα σε ένα string
    
    return text_string

# ********************* DEFS *********************

nlp = spacy.load("el_core_news_sm") 


# Φτιάχνει πίνακα με concordandces (με συγκεκριμένο πλάτος) με keyword   
def nltk_concordance(keyword, text_string):
    tokens = word_tokenize(text_string)
    text = nltk.Text(tokens)
    text.concordance(keyword, width=120, lines=20)
# Φτιάχνει πίνακα με concordandces (με συγκεκριμένο πλάτος λέξεων) με keyword   
def nltk_concordance_words(text_string, keyword, width=5):
    tokens = word_tokenize(text_string)
    ci = ConcordanceIndex(tokens)
    offsets = ci.offsets(keyword)
    for i in offsets:
        left = " ".join(tokens[max(0, i-width):i])
        right = " ".join(tokens[i+1:i+width+1])
        print(f"{left} [{keyword}] {right}")
#### NER - διάφορα ####
def nlp_spacy_ner_show_entities():
    text = nltk_from_news_to_str()
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    for row in entities:
        print(row)
def nlp_spacy_ner_show_entities2(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    for row in entities:
        print(row)
def nlp_spacy_ner_filter_entities():
    text = nltk_from_news_to_str()
    doc = nlp(text)

    choice = input("filter by category. PERSON, GPE, ORG, PRODUCT, EVENT")


    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == f"{choice}"]
    for row in entities:
        print(row)
    
    return entities
def nlp_spacy_ner_filter_entities2(text):
    doc = nlp(text)

    choice = input("filter by category. PERSON, GPE, ORG, PRODUCT, EVENT")


    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == f"{choice}"]
    for row in entities:
        print(row)
    
    return entities
def nlp_spacy_ner_percentage_of_entities():
    text = nltk_from_news_to_str()
    text1 = str(text)
    doc = nlp(text1)
    entities_by_label = defaultdict(list)
    for ent in doc.ents:
        entities_by_label[ent.label_].append(ent.text)
    
    # Συνολικός αριθμός οντοτήτων
    total_entities = sum(len(ents) for ents in entities_by_label.values())

    # Υπολογισμός ποσοστού ανά κατηγορία
    percentages = {label: (len(ents)/total_entities)*100 for label, ents in entities_by_label.items()}

    # Εκτύπωση
    for label, pct in percentages.items():
        print(f"{label}: {pct:.1f}% ({len(entities_by_label[label])} occurrences)")


def nlp_spacy_ner_percentage_of_entities2(text):
    text1 = str(text)
    doc = nlp(text1)
    entities_by_label = defaultdict(list)
    for ent in doc.ents:
        entities_by_label[ent.label_].append(ent.text)
    
    # Συνολικός αριθμός οντοτήτων
    total_entities = sum(len(ents) for ents in entities_by_label.values())

    # Υπολογισμός ποσοστού ανά κατηγορία
    percentages = {label: (len(ents)/total_entities)*100 for label, ents in entities_by_label.items()}

    # Εκτύπωση
    for label, pct in percentages.items():
        print(f"{label}: {pct:.1f}% ({len(entities_by_label[label])} occurrences)")
def nlp_spacy_ner_grouped_entities():
    text = nltk_from_news_to_str()
    text1 = str(text)
    doc = nlp(text1)
    entities_by_label = defaultdict(list)
    for ent in doc.ents:
        entities_by_label[ent.label_].append(ent.text)
    for label, ents in entities_by_label.items():
        print(f"{label}: {ents} \n")

def nlp_spacy_ner_grouped_entities2(text):
    text1 = str(text)
    doc = nlp(text1)
    entities_by_label = defaultdict(list)
    for ent in doc.ents:
        entities_by_label[ent.label_].append(ent.text)
    for label, ents in entities_by_label.items():
        print(f"{label}: {ents} \n")

def nlp_spacy_ner_grouped_entities3(text):
    doc = nlp(str(text))

    entities_by_label = defaultdict(Counter)

    for ent in doc.ents:
        entities_by_label[ent.label_][ent.text] += 1

    for label, counter in entities_by_label.items():
        print(f"{label}:")
        for ent, count in counter.items():
            print(f"  {ent} ({count})")
        print()

    return entities_by_label

def nlp_ner_find_dates(text):
    results = search_dates(text, languages=['el'])
    for r in results:
        print(f"{r} \n") 
              
    print(f"στο κείμενο ===> {text}")
    return results

def nlp_spacy_ner_grouped_entities(text):
    text1 = str(text)
    doc = nlp(text1)
    entities_by_label = defaultdict(list)
    for ent in doc.ents:
        entities_by_label[ent.label_].append(ent.text)
    for label, ents in entities_by_label.items():
        print(f"{label}: {ents} \n")
    return entities_by_label

def nlp_spacy_ner_percentage_of_entities2(text):
    text1 = str(text)
    doc = nlp(text1)
    entities_by_label = defaultdict(list)
    for ent in doc.ents:
        entities_by_label[ent.label_].append(ent.text)
    
    # Συνολικός αριθμός οντοτήτων
    total_entities = sum(len(ents) for ents in entities_by_label.values())

    # Υπολογισμός ποσοστού ανά κατηγορία
    percentages = {label: (len(ents)/total_entities)*100 for label, ents in entities_by_label.items()}

    # Εκτύπωση
    for label, pct in percentages.items():
        print(f"{label}: {pct:.1f}% ({len(entities_by_label[label])} occurrences)")

# ψιλοαδιάφορο, απλά να υπάρχει το παρακάτω 
def spacy_noun_chunks():
    text = nltk_from_news_to_str()
    doc = nlp(text)
    noun_chunks = [(noun_chunk) for noun_chunk in doc.noun_chunks]
    for row in noun_chunks:
        print(row)


###### GENSIM ######

# μετατρέπει προτάσεις σε vectors και βρίσκει similarities (η συγκεκριμένη έχει φιξ τιμές)
def nlp_gensim_vector_sentences():
    sentences = [
        ["this", "is", "a", "sentence"],
        ["this", "is", "another", "sentence"]
    ]

    # Εκπαίδευση
    model = Word2Vec(sentences, vector_size=30, window=5, min_count=1, workers=4)

    # Αποθήκευση
    model.save("my_word2vec.model")

    # Χρήση
    print(model.wv.most_similar("another")) 
# μια συνάρτηση του chatgpt που δείχνει το που (;) τοποθετείται η κάθε λέξη 
def example_gpt_show_similarities():
    from gensim.models import Word2Vec
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt

    # Παράδειγμα με ένα μικρό corpus
    sentences = [
        ["γάτα", "σκύλος", "ποντίκι"],
        ["μήλο", "πορτοκάλι", "μπανάνα"],
        ["αυτοκίνητο", "λεωφορείο", "τρένο"],
    ]

    # Εκπαίδευση μοντέλου
    model = Word2Vec(sentences, vector_size=50, window=5, min_count=1, workers=4)

    # Παίρνουμε τις λέξεις και τα embeddings τους
    words = list(model.wv.index_to_key)
    X = model.wv[words]

    # Μειώνουμε τη διάσταση σε 2D με PCA
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)

    # Οπτικοποίηση
    plt.figure(figsize=(6, 6))
    plt.scatter(result[:, 0], result[:, 1])

    # Προσθέτουμε labels στις λέξεις
    for i, word in enumerate(words):
        plt.annotate(word, xy=(result[i, 0], result[i, 1]))

    plt.show()
# Πολύ βασική classification με gensim - παίρνει τις πρώτες 20 ειδήσεις από ΒΔ
def nlp_gensim_basic_classicification():
    x = sq_choose_txt_column_from_newstable_wtho_print()  # λίστα από tuples
    x_first = x[:50]
    documents = [row[0] for row in x_first]  # λίστα μόνο με τα strings

    # Tokenization
    texts = [doc.lower().split() for doc in documents]

    # Δημιουργία λεξικού και corpus
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # LDA μοντέλο
    lda = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)

    topics = lda.print_topics(num_words=4)
    # Εκτύπωση θεμάτων
    for topic in topics:
        print(topic)
#Το ίδιο με μια def που κάνει υποτίθεται και καθαρισμό από stopwords
def nlp_gensim_classification_with_stopwords():
    stop_words = set(stopwords.words("greek"))
    x = sq_choose_txt_column_from_newstable_wtho_print()  # λίστα από tuples
    x_first = x[:100]
    documents = [row[0] for row in x_first]
    def preprocess(text):
        doc = nlp(text.lower())
        tokens = [
            token.lemma_ for token in doc 
            if token.is_alpha and token.lemma_ not in stop_words
        ]
        return tokens
    texts = [preprocess(doc) for doc in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)
    for idx, topic in lda.print_topics(num_words=5):
        print(f"Topic {idx}: {topic}")



def nlp_find_dates_streamlit(user_text):
    results = search_dates(user_text, languages=['el'])
    for r in results:
        st.write(f"{r} \n") 
              

def extract_date_sentences(text):
    """
    Παίρνει κείμενο και τυπώνει τις προτάσεις που περιέχουν ημερομηνίες.
    Υποστηρίζει μορφές όπως: 12 Ιανουαρίου 2023 ή 21/06/2023
    """
    import re
    from nltk.tokenize import sent_tokenize
    import streamlit as st
    
    # regex για ημερομηνίες (π.χ. 12 Ιανουαρίου 2023)
    greek_months = "Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου"
    date_pattern_1 = re.compile(rf"\b\d{{1,2}}\s({greek_months})\s\d{{4}}\b")
    
    # regex για μορφή 21/06/2023
    date_pattern_2 = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")

    date_pattern_3 = re.compile(r"\b\d{1,2}/\d{1,2}")
    
    # χωρισμός σε προτάσεις
    sentences = sent_tokenize(text, language="english")  # λειτουργεί και για ελληνικό κείμενο
    
    # έλεγχος και τύπωμα
    for sentence in sentences:
        if date_pattern_1.search(sentence) or date_pattern_2.search(sentence) or date_pattern_3.search(sentence):
            st.write("\n", sentence)


def nlp_highlight(text):
    doc = nlp(text)
    html = displacy.render(doc, style="ent")

    custom_html = f"""
        <style>
        body {{
            font-family: "Noto Sans", "Arial", sans-serif;
            font-size: 16px;
        }}

        .entity {{
            font-weight: 600;
        }}

         .ent-type-DATE {{
        text-decoration: underline;
        text-decoration-thickness: 2px;
        text-underline-offset: 3px;
        }}
        
        </style>

       
        {html}
        """
    
    st.components.v1.html(custom_html, height=800, scrolling=True)


def nlp_similarity(text1,text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    sim = doc1.similarity(doc2)
    st.metric("Similarity", f"{sim:.3f}")


def concordance_table(tokens, keyword, window):
    rows = []
    for i, word in enumerate(tokens):
        if word.lower() == keyword.lower():
            left = " ".join(tokens[max(i-window, 0):i])
            right = " ".join(tokens[i+1:i+1+window])
            rows.append({
                "Left context": left,
                "Word": word,
                "Right context": right
            })
    return pd.DataFrame(rows)



# ********************* TEST AREA *********************

