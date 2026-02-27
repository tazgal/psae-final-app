import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from mod_01_enter_open import add_this_to_text 
from mod_02_scrap import news_scrap_newspaper3k_full


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


def read_parapolitika_all():
    vima = vimatodotis_unique()
    mouth = big_mouth_unique()
    apoc = apocryptografos_unique2()

    combined = "\n".join([str(vima), str(mouth), str(apoc)])
    return combined

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

def all_to_txt():
    vimatodotis_to_txt()
    bigmouth_to_txt()
    apocryptografos_to_txt()

######## RUN AREA #########

#read_parapolitika_all()
#vimatodotis_to_txt()
#bigmouth_to_txt()
#apocryptografos_to_txt()
#all_to_txt()