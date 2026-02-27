# ********************* ΒΙΒΛΙΟΘΗΚΕΣ *********************

import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
import webbrowser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from mod_01_enter_open import add_this_to_text 
from mod_02_scrap import news_scrap_newspaper3k_full
from mod_02_scrap import scr_open_scraped_news
import streamlit as st
import json



# ********************* DEFS *********************

# Η συνάρτηση επιστρέφει τους τίτλους που περιέχουν ένα συγκεκριμένο κριτήριο αναζήτησης (φιξαρισμένο όμως) από τις παρακάτω ιστοσελίδες
def read_news_titles_fix():
    urls = [
        "https://www.protothema.gr/",
        "https://www.in.gr/",
        "https://www.cnn.gr/",
        "https://www.naftemporiki.gr/",
        "https://www.capital.gr/"
        "https://www.kathimerini.gr/",
        "https://www.ot.gr/",
        "https://www.efsyn.gr/",
        "https://www.ieidiseis.gr/",
        "https://www.mononews.gr/"
    ]

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου"]
    search_2 = ['ΝΔ', 'πρωθυπουργός', "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης" 'ΣΥΡΙΖΑ', "Φάμελος" 'Νέα Αριστερά', "Κωνσταντοπούλου" 'ΚΚΕ' ]
    search_3 = ['Οικονομία', "οικονομία" 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Χατζηδάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα", "εταιρεία", ]
    search_4 = ['ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση","εμπορικός πόλεμος", "δασμοί"]
    
    x = input("filter by theme: 1. for Middle East \n 2. for politics \n 3. for economy \n 4. for geopolitics")
    
    if x == "1":
        x = search_1
    elif x == "2": 
        x = search_2
    elif x == "3": 
        x = search_3
    elif x == "4": 
        x = search_4
    else: 
        print("this is not a choice")

    title_all = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            titles = soup.find_all('h3')
            filtered_titles = [
                title.get_text().strip()
                for title in titles
                if any(keyword in title.get_text() for keyword in x)
            ]

            for title in filtered_titles:
                title_all.append({"Website": url, "Title": title})

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    print(titles_df)
    return(titles_df)

#αυτή γυρνάει τα λινκ των ειδήσεων 
def read_news_titles_with_links():
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

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου"]
    search_2 = ['ΝΔ', 'πρωθυπουργός', "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης", 'ΣΥΡΙΖΑ', "Φάμελος", 'Νέα Αριστερά', "Κωνσταντοπούλου", 'ΚΚΕ']
    search_3 = ['Οικονομία', "οικονομία", 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Χατζηδάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα"]
    search_4 = ['ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση","εμπορικός πόλεμος", "δασμοί"]
    
    x = input("filter by theme: 1. for Middle East \n 2. for politics \n 3. for economy \n 4. for geopolitics\n")
    
    if x == "1":
        x = search_1
    elif x == "2": 
        x = search_2
    elif x == "3": 
        x = search_3
    elif x == "4": 
        x = search_4
    else: 
        print("this is not a choice")
        return

    title_all = []

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

                    title_all.append({
                        #"Website": url,
                        "Title": text,
                        "Link": href
                    })

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    print(titles_df)
    return titles_df

#αυτή γυρνάει τα λινκ των ειδήσεων 
def read_news_links_for_st(x):
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

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου"]
    search_2 = ['ΝΔ', 'πρωθυπουργός', "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης", 'ΣΥΡΙΖΑ', "Φάμελος", 'Νέα Αριστερά', "Κωνσταντοπούλου", 'ΚΚΕ']
    search_3 = ['Οικονομία', "οικονομία", 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Χατζηδάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα"]
    search_4 = ['ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση","εμπορικός πόλεμος", "δασμοί"]
        
    if x == "MEast":
        x = search_1
    elif x == "Politics": 
        x = search_2
    elif x == "Economy": 
        x = search_3
    elif x == "Geopolitics": 
        x = search_4
    else: 
        print("this is not a choice")
        return

    title_all = []

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

                    title_all.append({
                        #"Website": url,
                        "Title": text,
                        "Link": href
                    })

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    print(titles_df)
    return titles_df

# Το ίδιο για streamlit
def read_titles_streamlit():
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

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου"]
    search_2 = ['ΝΔ', 'πρωθυπουργός', "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης", 'ΣΥΡΙΖΑ', "Φάμελος", 'Νέα Αριστερά', "Κωνσταντοπούλου", 'ΚΚΕ']
    search_3 = ['Οικονομία', "οικονομία", 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Χατζηδάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα"]
    search_4 = ['ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση","εμπορικός πόλεμος", "δασμοί"]
    
    x = input("filter by theme: 1. for Middle East \n 2. for politics \n 3. for economy \n 4. for geopolitics\n")
    
    if x == "1":
        x = search_1
    elif x == "2": 
        x = search_2
    elif x == "3": 
        x = search_3
    elif x == "4": 
        x = search_4
    else: 
        print("this is not a choice")
        return

    title_all = []

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

                    title_all.append({
                        #"Website": url,
                        "Title": text,
                        "Link": href
                    })

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    st.write(titles_df)
    return titles_df

# ====> Παραπολιτικά 

def vimatodotis():
    url = "https://www.tovima.gr/editor/vimatodotis/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Παράδειγμα: βρίσκεις τίτλους άρθρων με βάση το HTML tag & class
        titles = soup.find_all("h3", class_="o-head f-400 my-0 is-size-2 zonabold")
        times = soup.find_all(class_="line-height-1 mr-3 post-date updated manrope is-size-5 semigrey-c")
        urls = soup.find_all("a", class_="columns is-mobile is-multiline", href=True)  
        
        print("\n")
        print("Ο Βηματοδότης γράφει:")
        print("\n")

        for t,d, u in zip(titles,times, urls):
            print(t.get_text(strip=True))
            print(d.get_text(strip=True))
            print(u["href"])
            print("*"*20)
            print("\n")



        return titles, times, urls
    
    
    else:
        print("⚠️ Σφάλμα:", response.status_code)

def vimatodotis_unique():
    url = "https://www.tovima.gr/editor/vimatodotis/" 
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Παίρνουμε τον ΠΡΩΤΟ τίτλο (τελευταία ανάρτηση)
        title_tag = soup.find("h3", class_="o-head f-400 my-0 is-size-2 zonabold").get_text(strip=True)
        time_tag = soup.find(class_="line-height-1 mr-3 post-date updated manrope is-size-5 semigrey-c").get_text(strip=True)
        url = soup.find("a", class_="columns is-mobile is-multiline", href=True)
        url_clean = url["href"]

        print("-"*20)
        print("\nΟ Βηματοδότης γράφει:\n")
        print(title_tag)
        print(time_tag)
        print(url_clean)
        print("\n")
        print("-"*20)

        return title_tag,time_tag,url_clean

        
    else:
        print("⚠️ Σφάλμα:", response.status_code)


def vimatodotis_for_streamlit():
    url = "https://www.tovima.gr/editor/vimatodotis/" 
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Παίρνουμε τον ΠΡΩΤΟ τίτλο (τελευταία ανάρτηση)
        title_tag = soup.find("h3", class_="o-head f-400 my-0 is-size-2 zonabold").get_text(strip=True)
        time_tag = soup.find(class_="line-height-1 mr-3 post-date updated manrope is-size-5 semigrey-c").get_text(strip=True)
        url = soup.find("a", class_="columns is-mobile is-multiline", href=True)
        url_clean = url["href"]

        st.write("-"*20)
        st.write("\nΟ Βηματοδότης γράφει:\n")
        st.write(title_tag)
        st.write(time_tag)
        st.write(url_clean)
        st.write("\n")
        st.write("-"*20)

        return title_tag,time_tag,url_clean

        
    else:
        print("⚠️ Σφάλμα:", response.status_code)


def big_mouth():
    url = "https://www.powergame.gr/category/big-mouth/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Παράδειγμα: βρίσκεις τίτλους άρθρων με βάση το HTML tag & class
        titles = soup.find_all("h3", class_="o-head")
        times = soup.find_all("span", class_="post-date")
        urls = soup.find_all("a", class_="underlined", href=True)  
        
        print("\n")
        print("To big mouth γράφει:")
        print("\n")

        for t,d, u in zip(titles,times, urls):
            print(t.get_text(strip=True))
            print(d.get_text(strip=True))
            print(u["href"])
            print("*"*20)
            print("\n")



        return titles, times, urls
    
    
    else:
        print("⚠️ Σφάλμα:", response.status_code)

def big_mouth_unique():
    url = "https://www.powergame.gr/category/big-mouth/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Παράδειγμα: βρίσκεις τίτλους άρθρων με βάση το HTML tag & class
        title = soup.find("h3", class_="o-head")
        time = soup.find("span", class_="post-date")
        url_all = soup.find("a", class_="underlined", href=True)
        url = url_all["href"]  
        
        print("\n")
        print("To big mouth γράφει:")
        print("\n")
        print(title.get_text(strip=True))
        print(time.get_text(strip=True))
        print(url)
        print("-"*20)
        print("\n")



        return title, time, url
    
    
    else:
        print("⚠️ Σφάλμα:", response.status_code)

def big_mouth_for_streamlit():
    url = "https://www.powergame.gr/category/big-mouth/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Παράδειγμα: βρίσκεις τίτλους άρθρων με βάση το HTML tag & class
        title = soup.find("h3", class_="o-head")
        time = soup.find("span", class_="post-date")
        url_all = soup.find("a", class_="underlined", href=True)
        url = url_all["href"]  
        
        st.write("-"*20)
        st.write("\nTo big mouth γράφει:\n")
        st.write(str(title))
        st.write(str(time))
        st.write(str(url))
        st.write("\n")
        st.write("-"*20)

def big_mouth_for_streamlit2():
    url = "https://www.powergame.gr/category/big-mouth/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        title_tag = soup.find("h3", class_="o-head")
        time_tag  = soup.find("span", class_="post-date")
        url_all   = soup.find("a", class_="underlined", href=True)

        # Αν βρεθεί το <a>
        if url_all:
            post_url = url_all["href"]
        else:
            post_url = "⚠️ Δεν βρέθηκε σύνδεσμος"

        # Αν δεν υπάρχουν tags, βάζουμε κενό string για να μην σκάσει
        title_text = title_tag.get_text(strip=True) if title_tag else "⚠️ Δεν βρέθηκε τίτλος"
        time_text  = time_tag.get_text(strip=True)  if time_tag  else "⚠️ Δεν βρέθηκε ημερομηνία"

        st.write("To big mouth γράφει:")
        st.write(title_text)
        st.write(time_text)
        st.write(post_url)
        st.write("-"*20)



def apocryptografos():
    url = "https://www.newsit.gr/category/blogs/apocryptografos/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # βρίσκουμε τίτλους και ημερομηνίες
        titles = soup.find_all("h3", class_="article-title")
        times = soup.find_all("time", class_="fs-xs beige-dark-gray-text row wrap start-center gap-xs")
          
        print("\nΟ apocryptografos (newsit) γράφει:\n")

        results = []  # εδώ θα μαζέψουμε τα δεδομένα

        for t, d in zip(titles, times):
            a = t.find("a", href=True)          # βρίσκουμε το <a> μέσα στο <h3>
            title_text = a.get_text(strip=True) if a else t.get_text(strip=True)
            link = urljoin(url, a["href"]) if a else None

            print(title_text)
            print(d.get_text(strip=True))
            print(link)
            print("*" * 20)
            print("\n")

            results.append({
                "title": title_text,
                "time": d.get_text(strip=True),
                "url": link
            })

        return results
    
    else:
        print("⚠️ Σφάλμα:", response.status_code)
        return []

def apocryptografos_unique():
    url = "https://www.newsit.gr/category/blogs/apocryptografos/" 
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # βρίσκουμε τίτλους και ημερομηνίες
        titles = soup.find("h3", class_="article-title")
        times = soup.find("time", class_="fs-xs beige-dark-gray-text row wrap start-center gap-xs")
          
        print("\n Ο apocryptografos (newsit) γράφει:\n")

        
        a = titles.find("a", href=True)          # βρίσκουμε το <a> μέσα στο <h3>
        title_text = a.get_text(strip=True) if a else titles.get_text(strip=True)
        link = urljoin(url, a["href"]) if a else None


        print(title_text)
        print(times.get_text(strip=True))
        print(link)
        print("-" * 20)
        print("\n")

        return titles, times, link

    
    else:
        print("⚠️ Σφάλμα:", response.status_code)
        return []

def apocryptografos_unique2():
    url = "https://www.newsit.gr/category/blogs/apocryptografos/" 
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        title_tag = soup.find("h3", class_="article-title")
        time_tag = soup.find("time", class_="fs-xs beige-dark-gray-text row wrap start-center gap-xs")

        if title_tag:
            a = title_tag.find("a", href=True)
            if a:
                title_text = a.get_text(strip=True)
                link = urljoin(url, a["href"])
                time_text = time_tag.get_text(strip=True) if time_tag else "—"

            print("\n Ο apocryptografos (newsit) γράφει:\n")
            print(title_text)
            print(time_text)
            print(link)
            print("-" * 20)
            print("\n")

                # 👉 εδώ επιστρέφουμε ΟΛΑ σαν strings
            return title_text, time_text, link
    
    return None, None, None

def apocryptografos_for_streamlit():
    url = "https://www.newsit.gr/category/blogs/apocryptografos/" 
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        title_tag = soup.find("h3", class_="article-title")
        time_tag = soup.find("time", class_="fs-xs beige-dark-gray-text row wrap start-center gap-xs")

        if title_tag:
            a = title_tag.find("a", href=True)
            if a:
                title_text = a.get_text(strip=True)
                link = urljoin(url, a["href"])
                time_text = time_tag.get_text(strip=True) if time_tag else "—"

            st.write("\n Ο apocryptografos (newsit) γράφει:\n")
            st.write(title_text)
            st.write(time_text)
            st.write(link)
            st.write("-" * 20)
            st.write("\n")

                # 👉 εδώ επιστρέφουμε ΟΛΑ σαν strings
            return title_text, time_text, link
    
    return None, None, None

def read_parapolitika_all():
    vima = vimatodotis_unique()
    mouth = big_mouth_unique()
    apoc = apocryptografos_unique2()

    combined = "\n".join([str(vima), str(mouth), str(apoc)])
    return combined

def read_parapolitika_all_streamlit():
    vimatodotis_for_streamlit()
    big_mouth_for_streamlit2()
    apocryptografos_for_streamlit()

def add_this_to_text(x, added_text):
    
    with open(f"{x}.txt", "a", encoding="utf-8") as f:
        content = f.write(added_text)
        print(added_text)
        return content

def vimatodotis_to_txt():
    url = vimatodotis_unique()[2]
    result = news_scrap_newspaper3k_full(url)["text"]
    add_this_to_text("parapolitika", "\n"*3)
    add_this_to_text("parapolitika", "-"*20)
    add_this_to_text("parapolitika", "Ο Βηματοδότης γράφει")
    add_this_to_text("parapolitika", result)

def bigmouth_to_txt():
    url = big_mouth_unique()[2]
    result = news_scrap_newspaper3k_full(url)["text"]
    add_this_to_text("parapolitika", "\n"*3)
    add_this_to_text("parapolitika", "-"*20)
    add_this_to_text("parapolitika", "Η στήλη Big Mouth γράφει")
    add_this_to_text("parapolitika", "\n"*3)
    add_this_to_text("parapolitika", result)

def apocryptografos_to_txt():
    url = apocryptografos_unique2()[2]
    result = news_scrap_newspaper3k_full(url)["text"]
    add_this_to_text("parapolitika", "\n"*3)
    add_this_to_text("parapolitika", "-"*20)
    add_this_to_text("parapolitika", "Ο apocryptografos γράφει")
    add_this_to_text("parapolitika", "\n"*3)
    add_this_to_text("parapolitika", result)

def read_news_parapolitika_all_to_txt():
    vimatodotis_to_txt()
    bigmouth_to_txt()
    apocryptografos_to_txt()

# ==> Οικονομικές ειδήσεις, απλά άνοιγμα
    
def rn_open_greek_economy_news():
    webbrowser.open("https://www.ot.gr")
    webbrowser.open("https://www.naftemporiki.gr/finance/economy/")
    webbrowser.open("https://www.kathimerini.gr/economy/")
    webbrowser.open("https://www.capital.gr/oikonomia")

def rn_show_greek_economy_news_radio():
    st.title("Οικονομικές Ειδήσεις")
    news_sites = {
        "OT.gr": "https://www.ot.gr",
        "Ναυτεμπορική": "https://www.naftemporiki.gr/finance/economy/",
        "Καθημερινή": "https://www.kathimerini.gr/economy/",
        "Capital": "https://www.capital.gr/oikonomia"
    }

    choice = st.radio("Επίλεξε ιστοσελίδα:", list(news_sites.keys()))
    
    if st.button("Άνοιγμα σελίδας"):
        webbrowser.open(news_sites[choice])

    if st.button("Άνοιγμα όλων μαζί"):
        for url in news_sites.values():
            webbrowser.open(url)

def rn_show_greek_economy_news_buttons():
    st.subheader("Οικονομικές Ειδήσεις")
    
    news_sites = {
        "OT.gr": "https://www.ot.gr",
        "Ναυτεμπορική": "https://www.naftemporiki.gr/finance/economy/",
        "Καθημερινή": "https://www.kathimerini.gr/economy/",
        "Capital": "https://www.capital.gr/oikonomia"
    }

    for i, (name, url) in enumerate(news_sites.items()):
        if st.button(name, key=f"news_{i}"):
            webbrowser.open(url)

        st.divider()

    if st.button("📂 Άνοιγμα οικονομικών", key="open_all"):
        for url in news_sites.values():
            webbrowser.open(url)

    
def rn_global_economy_news():
    webbrowser.open("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen")
    webbrowser.open("https://www.investopedia.com/")
    webbrowser.open("https://www.naftemporiki.gr/finance/world/")
    webbrowser.open("https://www.oecd.org/")
    webbrowser.open("https://www.imf.org/en/Home")
    webbrowser.open("https://www.imf.org/en/Whats-New-Archive")
    webbrowser.open("https://www.worldbank.org/en/home")
    webbrowser.open("https://www.pmi.spglobal.com/")
    webbrowser.open("https://www.marketwatch.com/")
    webbrowser.open("https://economictimes.indiatimes.com")


def rn_global_economy_news_buttons():
    st.subheader("Global Economy News")

    news_sites = {
        "Google News (Economy)": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
        "Investopedia": "https://www.investopedia.com/",
        "Ναυτεμπορική (World)": "https://www.naftemporiki.gr/finance/world/",
        "OECD": "https://www.oecd.org/",
        "IMF Home": "https://www.imf.org/en/Home",
        "IMF What's New": "https://www.imf.org/en/Whats-New-Archive",
        "World Bank": "https://www.worldbank.org/en/home",
        "S&P Global PMI": "https://www.pmi.spglobal.com/",
        "MarketWatch": "https://www.marketwatch.com/",
        "Economic Times": "https://economictimes.indiatimes.com"
    }

    cols = st.columns(2)
    for i, (name, url) in enumerate(news_sites.items()):
        with cols[i % 2]:
            if st.button(f"{name}"):
                webbrowser.open(url)

    if st.button("🚀 Άνοιγμα παγκόσμιων οικονομικών"):
        for url in news_sites.values():
            webbrowser.open(url)


def rn_economy_news_buttons():
    st.title("Economy News")

    news_sites = {
        "OT.gr": "https://www.ot.gr",
        "Ναυτεμπορική": "https://www.naftemporiki.gr/finance/economy/",
        "Καθημερινή": "https://www.kathimerini.gr/economy/",
        "Capital": "https://www.capital.gr/oikonomia",
        
    }

    cols = st.columns(2)
    for i, (name, url) in enumerate(news_sites.items()):
        with cols[i % 2]:
            if st.button(f"{name}"):
                webbrowser.open(url)

    if st.button("Άνοιγμα όλων των οικονομικών"):
        for url in news_sites.values():
            webbrowser.open(url)


def rn_global_economy_news_tabs():
    st.title("Global Economy News")

    news_sites = {
        "Google News (Economy)": "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
        "Investopedia": "https://www.investopedia.com/",
        "Ναυτεμπορική (World)": "https://www.naftemporiki.gr/finance/world/",
        "OECD": "https://www.oecd.org/",
        "IMF Home": "https://www.imf.org/en/Home",
        "IMF What's New": "https://www.imf.org/en/Whats-New-Archive",
        "World Bank": "https://www.worldbank.org/en/home",
        "S&P Global PMI": "https://www.pmi.spglobal.com/",
        "MarketWatch": "https://www.marketwatch.com/",
        "Economic Times": "https://economictimes.indiatimes.com"
    }

    tabs = st.tabs(list(news_sites.keys()))
    for i, (name, url) in enumerate(news_sites.items()):
        with tabs[i]:
            st.markdown(f"👉 [Άνοιγμα {name}]({url})")


def rn_show_general_news():
    st.subheader("Γενικά Νέα")
    
    news_sources = {
    "ERT News": "https://www.ertnews.gr",
    "In.gr": "https://www.in.gr",
    "IEidiseis": "https://www.ieidiseis.gr",
    "Iefimerida": "https://www.iefimerida.gr",
    "Naftemporiki": "https://www.naftemporiki.gr",
    "Capital": "https://www.capital.gr",
    "Kathimerini": "https://www.kathimerini.gr",
    "Ethnos": "https://www.ethnos.gr"
}


    for name, url in news_sources.items():
        if st.button(name):
            webbrowser.open(url)

    st.divider()

    if st.button("📂 Άνοιγμα γενικών"):
        for url in news_sources.values():
            webbrowser.open(url)


def rn_show_diethni_news():
    st.subheader("Γενικά Νέα")
    
    international_sources = {
    "Axios": "https://www.axios.com/",
    "Al Jazeera": "https://www.aljazeera.com/",
    "Reuters World": "https://www.reuters.com/news/world",
    "BBC Monitoring – Global News": "https://monitoring.bbc.co.uk/",
    "Al Jazeera | Crisis Zones": "https://www.aljazeera.com/news/",
    "CNN":"https://edition.cnn.com",
    "Bild":"https://www.bild.de",
    "DW":"https://www.dw.com/en/top-stories/s-9097",
    "Liberation":"https://www.liberation.fr",
    "El Pais":"https://elpais.com",
    "La Vanguardia":"https://www.lavanguardia.com",
    "Repubblica":"https://www.repubblica.it",
    "Corriera":"https://www.corriere.it"


}



    for name, url in international_sources.items():
        if st.button(name):
            webbrowser.open(url)

    st.divider()

    if st.button("📂 Άνοιγμα διεθνών"):
        for url in international_sources.values():
            webbrowser.open(url)


def rn_show_geopolitics_news():
    st.subheader("Γεωπολιτικά Νέα")
    
    geopolitics_sources = {
    "NATO": "https://www.nato.int/",
    "Atlantic Council": "https://www.atlanticcouncil.org/",
    "Global Research": "https://www.globalresearch.ca/",
    "The Cradle": "https://new.thecradle.co/",
    "IISS (International Institute for Strategic Studies)": "https://www.iiss.org/",
    "The Conversation (Europe)": "https://theconversation.com/europe",
    "Foreign Affairs": "https://www.foreignaffairs.com/",
    "WarNews247": "https://warnews247.gr/",
    "SETA Think Tank (Turkey)": "https://www.setav.org/en/",
    "ECFR (European Council on Foreign Relations)": "https://ecfr.eu/about/",
    "Geopolitical Futures": "https://geopoliticalfutures.com/welcome/",
    "Middle East Program | Wilson Center": "https://www.wilsoncenter.org/program/middle-east-program",
    "Bloomberg Geopolitics": "https://www.bloomberg.com/politics",
    "Arab Center Washington DC": "https://arabcenterdc.org/",
    "Essydo": "https://essydo.com/",
    "Twitter: @BePanos4471": "https://twitter.com/BePanos4471"
}



    for name, url in geopolitics_sources.items():
        if st.button(name):
            webbrowser.open(url)

    st.divider()

    if st.button("📂 Άνοιγμα γεωπολιτικών"):
        for url in geopolitics_sources.values():
            webbrowser.open(url)

def rn_show_brics_news():
    st.subheader("Νέα ευρασιατικού")
    
    eurasia_sources = {
    "People’s Daily (China)": "http://en.people.cn/index.html",
    "Twitter: @IndoPac_Info (Indo-Pacific Updates)": "https://twitter.com/IndoPac_Info",
    "Twitter: @maxseddon (FT Moscow Bureau Chief)": "https://twitter.com/maxseddon",
    "Institute of World Economics and Politics (CASS, China)": "https://www.iwep.org.cn/",
    "China Law Translate": "https://www.chinalawtranslate.com/",
    "SCO (Shanghai Cooperation Organisation)": "https://eng.sectsco.org/",
    "BRICS Affairs": "https://bricsaffairs.gr/",
    "Kosmodromio": "https://kosmodromio.gr/"
}




    for name, url in eurasia_sources.items():
        if st.button(name):
            webbrowser.open(url)

    st.divider()

    if st.button("📂 Άνοιγμα ευρασιατικών"):
        for url in eurasia_sources.values():
            webbrowser.open(url)


 
def rn_vouli():
    webbrowser.open("https://www.hellenicparliament.gr/Nomothetiko-Ergo/dailyplan")
    webbrowser.open("https://www.hellenicparliament.gr/Koinovouleftikes-Epitropes/Evdomadiaio-Deltio")

def rn_radios():
    webbrowser.open("https://live24.gr/radio/realfm")
    webbrowser.open("https://live24.gr/radio/generic.jsp?sid=1986")

def read_titles_geopol_streamlit():
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

    search_1 = ['Συρία', 'Δαμασκός', 'Άσαντ', 'αντάρτες', 'πόλεμος', "Τουρκία", "Ιράν","Ισραήλ", "Ουκρανία","Ρωσία", "Γάζα", "Νετανιάχου", 'ΗΠΑ', 'Τράμπ', 'Γερμανία', "Γαλλία", "Ιταλία", "ευρωζώνη", "Ρωσία", "Κίνα", "ΝΑΤΟ", "ΕΕ", "Ευρωπαϊκή Ενωση","εμπορικός πόλεμος", "δασμοί"]
       
    x = search_1
    
    title_all = []

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

                    title_all.append({
                        #"Website": url,
                        "Title": text,
                        "Link": href
                    })

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    st.write(titles_df)
    return titles_df

def read_titles_pol_streamlit():
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

    search_1 = ['ΝΔ', 'πρωθυπουργός', "κυβέρνηση", "Μητσοτάκης", 'ΠΑΣΟΚ', "Ανδρουλάκης" 'ΣΥΡΙΖΑ', "Φάμελος" 'Νέα Αριστερά', "Κωνσταντοπούλου" 'ΚΚΕ' ]

       
    x = search_1
    
    title_all = []

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

                    title_all.append({
                        #"Website": url,
                        "Title": text,
                        "Link": href
                    })

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    st.write(titles_df)
    return titles_df

def read_titles_economy_streamlit():
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

    search_1 = ['Οικονομία', "οικονομία" 'προϋπολογισμός', 'κέρδη', "εταιρεία", "Χατζηδάκης", "φόροι", "ακρίβεια", "πληθωρισμός", "παραγωγικότητα", "εταιρεία", ]

       
    x = search_1
    
    title_all = []

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

                    title_all.append({
                        #"Website": url,
                        "Title": text,
                        "Link": href
                    })

    titles_df = pd.DataFrame(title_all)

    pd.set_option('display.max_colwidth', None)
    st.write(titles_df)
    return titles_df


def rizos_apopsi():
    url = "https://www.rizospastis.gr" 
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        apopsi = soup.find(class_="story_column")
        title_tag = soup.find(class_="title4")
        title = title_tag.get_text(strip=True)
        paragraphs = apopsi.find_all("p")
        
        st.write("-"*20)
        st.write("\nΗ Αποψη του «Ρ» σήμερα:\n")
        st.write(title)
        for p in paragraphs:
            text = p.get_text(strip=True)
            st.write(text)
        st.write("\n")
        st.write("-"*20)

        return apopsi

        
    else:
        print("⚠️ Σφάλμα:", response.status_code)


# ********************* TEST AREA *********************

def rn_dieftinseis():
    news_df = pd.read_json("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/lexika/newsid.json")

    categories = news_df.category.unique().tolist()
    categories = ["All"] + categories

    selected_category = st.selectbox("Select category", categories)

    filtered_df = news_df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df.category == selected_category]

    st.dataframe(filtered_df)


def rn_open_dieftinseis():
    news_df = pd.read_json("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/lexika/newsid.json")

    categories = news_df.category.unique().tolist()
    categories = ["All"] + categories

    selected_category = st.selectbox("Select category", categories)

    filtered_df = news_df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df.category == selected_category]

    open_button = st.button(f"open {filtered_df}")
    
    if open_button:
        st.dataframe(filtered_df)



def rn_sources_selector():
    
    with open("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/lexika/newsid.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        st.warning("Το αρχείο δεν περιέχει δεδομένα.")
        return

    # Όλες οι κατηγορίες (+ "Όλες")
    categories = sorted({item["category"] for item in data})
    categories.insert(0, "Όλες")

    selected_category = st.selectbox(
        "Φιλτράρισμα ανά κατηγορία",
        categories,
        key="category_filter"
    )

    # Φιλτραρισμένα δεδομένα
    if selected_category == "Όλες":
        filtered_data = data
    else:
        filtered_data = [
            item for item in data if item["category"] == selected_category
        ]

    if not filtered_data:
        st.info("Δεν υπάρχουν πηγές για αυτή την κατηγορία.")
        return

    # Mapping name → url
    name_to_url = {item["name"]: item["url"] for item in filtered_data}

    selected_name = st.selectbox(
        "Επίλεξε πηγή",
        list(name_to_url.keys()),
        key="source_selector"
    )

    selected_url = name_to_url[selected_name]

    # Κουμπί που ανοίγει το link
    st.link_button(
        "Άνοιγμα πηγής στον browser",
        selected_url
    )

    if st.button("🚀 Άνοιγμα όλων των πηγών"):
        for item in filtered_data:
            webbrowser.open(item["url"])

@st.cache_data
def rn_load_sources():
    with open("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_2/data/lexika/newsid.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def rn_sources_by_category(df, category):
    return df[df["category"] == category]


def render_sources_selector_arxiko(df, category, label):
    df_cat = df[df["category"] == category]

    if df_cat.empty:
        st.info("Δεν υπάρχουν πηγές.")
        return

    source = st.selectbox(label, df_cat["name"].tolist())
    url_source = df_cat[df_cat["name"] == source]["url"].values[0]


    st.link_button("Άνοιγμα πηγής", url_source)

def render_sources_selector(
    df,
    category,
    label,
    state_key="selected_url",
    subcategory=None
):
    df_cat = df[df["category"] == category]

    if subcategory:
        df_cat = df_cat[df_cat["subcategory"] == subcategory]

    if df_cat.empty:
        st.info("Δεν υπάρχουν πηγές για αυτή την επιλογή.")
        return

    source = st.selectbox(
        label,
        df_cat["name"].tolist(),
        key=f"{category}_{subcategory}_selector"
    )

    url_source = df_cat.loc[
        df_cat["name"] == source, "url"
    ].values[0]

    st.session_state[state_key] = url_source

    st.link_button(
        "🌐 Άνοιγμα πηγής σε νέο tab",
        url_source
    )

