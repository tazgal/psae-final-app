#Δεν είναι έτοιμος ακόμα

import pandas as pd

News_df = pd.DataFrame(columns=['Title', 'Date', 'Text', 'Summary', 'Keywords', "url"])

def new_row():
    new_row = [Τίτλος, Ημερομηνία, Κείμενο, Σύνοψη, Keywords, url]

    News_df.loc[len(News_df)] = new_row

new_row()
print(News_df)


