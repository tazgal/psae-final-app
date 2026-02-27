
text1 = ("This is a text", "this is a second text", "this is nothing")
text2 = ("This is summer", "this is not summer", "this is winter")

choose_text = input("Διαλέξτε κείμενο text1 ή text2")

keywords1 = ["nothing"]
keywords2 = input("please enter keywords split by comma")
keywords2 = keywords2.split(",")

if choose_text == "text1":
    text = text1
elif choose_text == "text2":
    text = text2
else:
    print("Μη έγκυρη επιλογή, θα χρησιμοποιήσω text1")
    text = text1

def search_keyword(text, keywords):
    for t in text: 
        for keyword in keywords:
            if keyword in t: 
                print(t)

search_keyword(text,keywords2)