###### Πάρε τίτλους από naftemporiki και ψάξε με λέξεις κλειδιά #######
## https://www.naftemporiki.gr/newsroom/

from bs4 import BeautifulSoup
import requests

def πάρε_τίτλους(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h2", class_="item-title")

        τίτλοι = []
        for title in titles:
            τίτλοι.append(title.text.strip())  # .strip() για καθαρό κείμενο χωρίς περιττά κενά
        return τίτλοι
    else:
        return []


url = input("Enter the URL of the article: ")

πάρε_τίτλους(url)

keywords = input("Βάλε λέξεις κλειδιά χωρισμένες με κόμμα: ")
keywords = keywords.split(",")

τίτλοι = πάρε_τίτλους("https://www.naftemporiki.gr/kosmos/")

for title in τίτλοι:
  if any(keyword in title for keyword in keywords):
    print(title.strip())
