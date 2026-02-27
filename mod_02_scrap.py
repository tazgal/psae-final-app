import requests
from bs4 import BeautifulSoup
import nltk
import newspaper
from newspaper import Article
from mod_01_enter_open import enter_url, enter_urls
import webbrowser
import streamlit as st


# Μια συνάρτηση που παίρνει url και με Newspaper3k επιστρέφει τίτλο κτλ (ως λεξικό)
def news_scrap_newspaper3k_full(url): 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    title = article.title
    date = article.publish_date
    text = article.text
    summary = article.summary
    keywords = article.keywords
    image = article.top_image

    print("----- αρχή είδησης ------")
    print("\n")
    print(f"Τίτλος: {title}")
    print("\n")
    print(f"Ημερομηνία: {date}")
    print("\n")
    print(f"Κείμενο: {text}")
    print("\n")
    print(f"Σύνοψη: {summary}")
    print("\n")
    print(f"Λέξεις κλειδιά: {keywords}")
    print(keywords)
    print("\n")
    print(image)
    print("\n")
    print("----- τέλος είδησης ------")
    
    news_line = {
    
    "title": title,
    "date": date,
    "url": url,
    "text": text,
    "summary": summary,
    "keywords": ", ".join(keywords)  

    }

    return news_line

def news_newspaper3k_streamlit(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    title = article.title
    date = article.publish_date
    text = article.text
    summary = article.summary
    keywords = article.keywords
    image = article.top_image

    
    st.write(title)
    st.write(text)


def news_scrap_newspaper3k_full_wth_print(url): 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    title = article.title
    date = article.publish_date
    text = article.text
    summary = article.summary
    keywords = article.keywords

    
    news_line = {
    
    "title": title,
    "date": date,
    "url": url,
    "text": text,
    "summary": summary,
    "keywords": ", ".join(keywords)  

    }

    return news_line

# Μια συνάρτηση μόνο για τίτλο
def news_scrap_title(url): 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    title = article.title
    print(title)
    return(title)

def news_scrap_text(url): 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    text = article.text
    print(text)
    return(text)

# Μια συνάρτηση όπου διαλέγεις αν θα κάνεις scrap τίτλο ή κείμενο 
def news_scrap_choose(url): 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    choose = input("Choose what to scrap: \n 1 = title, 2 = text ")
    if choose == "1":
        print(article.title)
        return article.title
    elif choose == "2":
        print(article.text)
        return article.text
    else:
        print("this is not a choice")


# Μια συνάρτηση που παίρνει url και με Newspaper3k επιστρέφει ό,τι εσύ επιλέγεις πχ τίτλο  
def news_scrap_choose(url): 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    choose = input("Choose what to scrap: \n 1 = title, 2 = text")
    if choose == "1":
        print(article.title)
        return article.title
    elif choose == "2":
        print(article.text)
        return article.text
    else:
        print("this is not a choice")

#Μια συνάρτηση που κάνει extract μια λίστα με τους τίτλους των urls που της βάζεις 
def extract_list_titles(): 
    titles_list = []
    urls = enter_urls()
    for url in urls:
        x = news_scrap_title(url)
        titles_list.append(x)
    print(titles_list)
    return(titles_list)

# Μια συνάρτηση που κάνει scrap με requests σε συγκεκριμένες ιστοσελίδες και με συγκεκριμένες λέξειες κλειδιά
# και επιστρέφει σε λίστα τα urls 
def scrap_news_return_links():
    urls = [
        "https://www.protothema.gr/",
        "https://www.in.gr/",
        "https://www.cnn.gr/",
        "https://www.naftemporiki.gr/",
        "https://www.capital.gr/",
        "https://www.kathimerini.gr/",
        "https://www.ot.gr/",
        "https://www.efsyn.gr/",
        "https://www.ieidiseis.gr/",
        "https://www.mononews.gr/"
    ]

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου","Παλαιστίνη",'ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση"]
    search_2 = ['ΝΔ', 'πρωθυπουργός',"κυβέρνηση", "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης", 'ΣΥΡΙΖΑ', "Φάμελος", 'Νέα Αριστερά', "Κωνσταντοπούλου", 'ΚΚΕ']
    search_3 = ['Οικονομία', "οικονομία", 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Πιερρακάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα","εμπορικός πόλεμος", "δασμοί"]
    
    x = input("filter by theme: 1. for Middle East - Ukraine - geopolitics \n 2. for politics \n 3. for economy")
    
    if x == "1":
        x = search_1
    elif x == "2": 
        x = search_2
    elif x == "3": 
        x = search_3
    else: 
        print("this is not a choice")
        return

    news_urls = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            titles = soup.find_all('h3')
            for t in titles:
                text = t.get_text().strip()
                if any(keyword in text for keyword in x):
                    link = t.find('a')
                    href = link['href'] if link else None

                    # αν το href είναι σχετικό (π.χ. "/politics/..."), το κάνουμε πλήρες
                    if href and href.startswith("/"):
                        href = url.rstrip("/") + href

                    news_urls.append(href)
    
    print(news_urls)
    return news_urls

def scrap_news_return_links2(choice):
    urls = [
        "https://www.protothema.gr/",
        "https://www.in.gr/",
        "https://www.cnn.gr/",
        "https://www.naftemporiki.gr/",
        "https://www.capital.gr/",
        "https://www.kathimerini.gr/",
        "https://www.ot.gr/",
        "https://www.efsyn.gr/",
        "https://www.ieidiseis.gr/",
        "https://www.mononews.gr/"
    ]

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου","Παλαιστίνη",'ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση"]
    search_2 = ['ΝΔ', 'πρωθυπουργός',"κυβέρνηση", "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης", 'ΣΥΡΙΖΑ', "Φάμελος", 'Νέα Αριστερά', "Κωνσταντοπούλου", 'ΚΚΕ']
    search_3 = ['Οικονομία', "οικονομία", 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Πιερρακάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα","εμπορικός πόλεμος", "δασμοί"]
    
    choices = {
        "1": search_1,
        "2": search_2,
        "3": search_3,
    }

    if choice not in choices:
        print("Λάθος επιλογή")
        return []

    keywords = choices[choice]
    news_urls = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('h3')
            for t in titles:
                text = t.get_text().strip()
                if any(keyword in text for keyword in keywords):
                    link = t.find('a')
                    href = link['href'] if link else None

                    if href:  # αν υπάρχει σύνδεσμος
                        if href.startswith("/"):
                            href = url.rstrip("/") + href
                        news_urls.append(href)
    
    return news_urls

# Κάνει build ιστοσελίδα και ανοίγει τα urls
def scr_newspaper_build(url):

    news = newspaper.build(url)

    for article in news.articles[0:2]:
        try:
            article.download()
            article.parse()
            print(article.title)
            print(article.url)

            # άνοιξε το άρθρο στον browser
            webbrowser.open(article.url)

            print("----------")
        except Exception as e:
            print(f"Πρόβλημα με άρθρο: {e}")

# Ανοίγει στον browser τους τίτλους που κάνει scrap με τα κριτήρια
def scr_open_scraped_news():
    links = scrap_news_return_links()
    for link in links:
        webbrowser.open(f"{link}")

def scrape_evdomadiaio_deltio_html():
    url = "https://www.hellenicparliament.gr/Koinovouleftikes-Epitropes/Evdomadiaio-Deltio"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    pagecontent = soup.find("div", class_="pagecontent")

    if not pagecontent:
        return None

    return str(pagecontent)

def scrap_praktika():
    url = "https://www.hellenicparliament.gr/Praktika/Synedriaseis-Olomeleias"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    tbody = soup.select_one("#pagecontent table tbody")

    if not tbody:
        return None

    return str(tbody)


def scrap_praktika_structured():
    url = "https://www.hellenicparliament.gr/Praktika/Synedriaseis-Olomeleias"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("#pagecontent table tbody tr")

    results = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        date = cols[0].get_text(strip=True)
        link_tag = cols[1].find("a")

        title = link_tag.get_text(strip=True) if link_tag else ""
        link = link_tag["href"] if link_tag else ""

        if link and link.startswith("/"):
            link = "https://www.hellenicparliament.gr" + link

        results.append({
            "date": date,
            "title": title,
            "url": link
        })

    return results

# ********************* TEST AREA *********************

