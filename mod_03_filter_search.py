import re
import os
from mod_01_enter_open import open_text, open_text_sp


# Ενα πολύ απλό search 
def simple_search(keyword, text):
    s_list = []
    sentences = text.split(".")
    keyword = keyword.strip()
    for sentence in sentences:
        clean_sent = sentence.strip()
        if keyword in clean_sent:
            s_list.append(clean_sent)

    return s_list
    


# Βασική regex που ψάχνει μια λέξη κλειδί σε ένα κείμενο 
def search_regex_word(text):
    # Χώρισε σε προτάσεις (με πιο σωστό διαχωρισμό)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    keyword = input("Which word do you want to search? ").strip()
    
    # Regex που ταιριάζει τη λέξη ακόμα και αν έχει σημεία στίξης μετά
    pattern = fr"\b{re.escape(keyword)}\b(?:[.,;]?)"
    
    # Βρες όλες τις προτάσεις που περιέχουν τη λέξη (case-sensitive)
    found_sentences = [s for s in sentences if re.search(pattern, s, flags=re.UNICODE)]
    
    if not found_sentences:
        print("No matches found.")
        return []
    
    for sentence in found_sentences:
        print(sentence)
    
    return found_sentences

# Συνάρτηση που ανοίγει αρχεία txt και ψάχνει με λέξεις κλειδιά
def open_and_search_files(keyword):

    folder = input("Please enter file path: ")
    os.chdir(folder)

    results = []

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            filename_without_ext = os.path.splitext(file)[0]
            text = open_text_sp(filename_without_ext)  # επιστρέφει string

            # Χώρισε σε προτάσεις
            sentences = re.split(r"(?<=[.!?])\s+", text)
            # Regex για την λέξη-κλειδί
            pattern = fr"(?:^|\s){keyword}(?=\s|$)"
            found_sentences = [s for s in sentences if re.search(pattern, s, flags=re.UNICODE)]

            if found_sentences:
                results.append((filename_without_ext, found_sentences))

    return results

def open_and_search_files2(keyword):
    folder = input("Please enter file path: ")
    os.chdir(folder)

    results = []

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            filename_without_ext = os.path.splitext(file)[0]

            # Άνοιγμα και διάβασμα του αρχείου
            with open(f"{file}", "r", encoding="utf-8") as f:
                text = f.read()

            # Χωρισμός σε προτάσεις
            sentences = re.split(r"(?<=[.!?])\s+", text)

            # Regex για τη λέξη-κλειδί
            pattern = fr"(?:^|\s){re.escape(keyword)}(?=\s|$)"

            # Επιλογή μόνο των προτάσεων που περιέχουν τη λέξη
            found_sentences = [s for s in sentences if re.search(pattern, s, flags=re.UNICODE)]

            if found_sentences:
                results.append((filename_without_ext, found_sentences))

    return results

