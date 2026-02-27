import os 
import pandas as pd
from mod_01_enter_open import add_text, add_text_sp, open_text, open_text_sp





def open_files_from_folder():
    folder = input("please enter file path:  ")
    os.chdir(f"{folder}")

    files = []

    for file in os.listdir(folder):  # παίρνουμε όλα τα αρχεία
        print("Found:", file)  # εμφάνιση ονόματος

        if file.endswith(".txt"):
            filename_without_ext = os.path.splitext(file)[0]  # κόβει το ".txt"
            text = open_text_sp(filename_without_ext)
            files.append(text)
    print(files)
    return files        

# Φόρτωσε υπάρχον CSV ή πες του να δημιουργήσει νέο DataFrame
def open_csv(csv_path):
    if os.path.exists(csv_path):
        news_df = pd.read_csv(csv_path)
        return news_df
    else:
        print("file does not exist - create one first")