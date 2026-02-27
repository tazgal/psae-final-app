from newspaper import Article
import nltk
import pandas as pd


# Βάλε εδώ το URL του άρθρου που θες να κατεβάσεις
url = input("Δώσε url: ")

def scrap(url):  # Πρόσθεσε το url ως παράμετρο
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Επιστροφή όλων των δεδομένων ως λεξικό
    return {
        'Τίτλος': article.title,
        'Ημερομηνία': article.publish_date,
        'Κείμενο': article.text,
        'Σύνοψη': article.summary,
        'Keywords': article.keywords,
        'url': url  # Προσθήκη του URL στα δεδομένα
    }


News_df = pd.DataFrame(columns=['Title', 'Date', 'Text', 'Summary', 'Keywords', "url"])

def new_row(data, df):  # Δέχεται τα δεδομένα και το DataFrame ως ορίσματα
    new_row = {
        'Title': data['Τίτλος'],
        'Date': data['Ημερομηνία'],
        'Text': data['Κείμενο'],
        'Summary': data['Σύνοψη'],
        'Keywords': data['Keywords'],
        'url': data['url']
    }
    # Προσθήκη νέας σειράς με pd.concat (πιο αποδοτικό από το .loc)
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

data = scrap(url)          # Κατέβασε το άρθρο
News_df = new_row(data, News_df)  # Πρόσθεσέ το στο DataFrame
print(News_df)
