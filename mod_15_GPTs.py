import os
import requests
from dotenv import load_dotenv
import streamlit as st
import re
from mistralai import Mistral


load_dotenv()  # Φορτώνει HF_TOKEN μία φορά

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def gpt_deepseek():
    user_input = input("Γράψε την ερώτηση σου: ")
    
    try:
        response = query({
            "messages": [{"role": "user", "content": user_input}],
            "model": "deepseek-ai/DeepSeek-R1:novita"
        })
        print(response["choices"][0]["message"]["content"])
    except requests.exceptions.HTTPError as e:
        print("Σφάλμα στο API:", e)


def gpt_deepseek_streamlit():
    st.title("Hugging Face GPT Demo")

    # Input από χρήστη
    user_input = st.text_area("Γράψε την ερώτηση σου:")

    if st.button("Στείλε ερώτηση"):
        if user_input.strip() == "":
            st.warning("Πληκτρολόγησε πρώτα την ερώτηση σου!")
        else:
            try:
                response = query({
                    "messages": [{"role": "user", "content": user_input}],
                    "model": "deepseek-ai/DeepSeek-R1:novita"
                })
                answer = response["choices"][0]["message"]["content"]
                st.subheader("Απάντηση:")
                st.write(answer)
            except requests.exceptions.HTTPError as e:
                st.error(f"Σφάλμα στο API: {e}")
            except KeyError:
                st.error("Απροσδόκητη μορφή απάντησης από το API.")

def gpt_deepseek_streamlit_short():
    st.title("Hugging Face GPT Demo")

    # Input από χρήστη
    user_input = st.text_area("Γράψε την ερώτηση σου:")

    if st.button("Απάντηση από Deepseek"):
        if user_input.strip() == "":
            st.warning("Πληκτρολόγησε πρώτα την ερώτηση σου!")
        else:
            try:
                response = query({
                    "messages": 
                    [{"role": "system", "content": "Απάντησε σύντομα και μόνο στα ελληνικά, χωρίς να εξηγείς τη λογική σου."},
                    {"role": "user", "content": user_input}],
                    "model": "deepseek-ai/DeepSeek-R1:novita"
                })
                answer = response["choices"][0]["message"]["content"]
                st.subheader("Απάντηση:")
                clean_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
                st.write(clean_answer)
            except requests.exceptions.HTTPError as e:
                st.error(f"Σφάλμα στο API: {e}")
            except KeyError:
                st.error("Απροσδόκητη μορφή απάντησης από το API.")

def gpt_deepseek_streamlit_short2(text):
    
    if text.strip() == "":
        st.warning("Πληκτρολόγησε πρώτα την ερώτηση σου!")
    else:
        try:
            response = query({
                "messages": 
                [{"role": "system", "content": "Απάντησε σύντομα και μόνο στα ελληνικά, χωρίς να εξηγείς τη λογική σου."},
                {"role": "user", "content": text}],
                "model": "deepseek-ai/DeepSeek-R1:novita"
            })
            answer = response["choices"][0]["message"]["content"]
            st.subheader("Απάντηση:")
            clean_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
            st.write(clean_answer)
        except requests.exceptions.HTTPError as e:
            st.error(f"Σφάλμα στο API: {e}")
        except KeyError:
            st.error("Απροσδόκητη μορφή απάντησης από το API.")



def gpt_deepseek_vasika_simeia(user_input):

    if user_input.strip() == "":
        st.warning("Πληκτρολόγησε πρώτα την ερώτηση σου!")
    else:
        try:
            response = query({
                "messages": 
                [{"role": "system", "content": "Δώσε τα βασικά σημεία αυτού του κειμένου σε bullets, στα ελληνικά, χωρίς extra εξηγήσεις."},
                {"role": "user", "content": user_input}],
                "model": "deepseek-ai/DeepSeek-R1:novita"
            })
            answer = response["choices"][0]["message"]["content"]
            st.subheader("Απάντηση:")
            clean_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
            st.write(clean_answer)
        except requests.exceptions.HTTPError as e:
            st.error(f"Σφάλμα στο API: {e}")
        except KeyError:
            st.error("Απροσδόκητη μορφή απάντησης από το API.")

def gpt_deepseek_diorthosi(user_input):

    if user_input.strip() == "":
        st.warning("Πληκτρολόγησε πρώτα το κείμενο!")
    else:
        try:
            response = query({
                "messages": 
                [{"role": "system", "content": "Κάνε ορθογραφική διόρθωση στο κείμενο, βάλε τόνους, κάνε τα εισαγωγικό σε αυτή τη μορφή «», χωρίς να αλλάξεις τίποτα σε διατυπώσεις κτλ. Επίσης δε χρειάζεται να εξηγείς τίποτα σε σχέση με το σκεπτικό σου"},
                {"role": "user", "content": user_input}],
                "model": "deepseek-ai/DeepSeek-R1:novita"
            })
            answer = response["choices"][0]["message"]["content"]
            st.subheader("Απάντηση:")
            clean_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
            st.write(clean_answer)
        except requests.exceptions.HTTPError as e:
            st.error(f"Σφάλμα στο API: {e}")
        except KeyError:
            st.error("Απροσδόκητη μορφή απάντησης από το API.")


def gpt_diorthosi2(user_input):

    if user_input.strip() == "":
        st.warning("Πληκτρολόγησε πρώτα το κείμενο!")
    else:
        try:
            response = query({
                "messages": 
                [{"role": "system", "content": "Κάνε ορθογραφική διόρθωση στο κείμενο, βάλε τόνους, κάνε τα εισαγωγικό σε αυτή τη μορφή «», χωρίς να αλλάξεις τίποτα σε διατυπώσεις κτλ. Επίσης δε χρειάζεται να εξηγείς τίποτα σε σχέση με το σκεπτικό σου"},
                {"role": "user", "content": user_input}],
                "model": "google/flan-t5-base"
            })
            answer = response["choices"][0]["message"]["content"]
            st.subheader("Απάντηση:")
            clean_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
            st.write(clean_answer)
        except requests.exceptions.HTTPError as e:
            st.error(f"Σφάλμα στο API: {e}")
        except KeyError:
            st.error("Απροσδόκητη μορφή απάντησης από το API.")


def query_hf(payload):

    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    HEADERS = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}


    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

    st.title("🤖 Δωρεάν Chatbot με FLAN-T5")

    user_input = st.text_area("Γράψε το κείμενό σου:")
    if st.button("Στείλε"):
        if user_input.strip() != "":
            output = query_hf({"inputs": user_input})
            st.subheader("Απάντηση:")
            st.write(output[0]["generated_text"])




def gpt_mistral_general(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    print(chat_response.choices[0].message.content)

def gpt_mistral_general_streamlit(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)

def gpt_mistral_diorthosi_streamlit(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "system",
            "content": "Είσαι ένας βοηθός που κάνει μόνο ορθογραφική διόρθωση στα ελληνικά. "
                       "Βάζεις τόνους, διορθώνεις ορθογραφικά λάθη, αλλά δεν αλλάζεις τη διατύπωση."
            },
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)

def gpt_mistral_plagios_streamlit(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "system",
            "content": "Είσαι ένας βοηθός που κάνει το εξής:"
                       "Σου δίνω ένα κείμενο - απομαγνητοφώνηση και μου το κάνεις σαν ρεπορτάζ"
                       "χρησιμοποιώντας πχ εκφράσεις όπως 'μεταξύ άλλων ο ομιλητής τόνισε πως', 'Οπως επισήμανε ο ομιλητής κτλ'"
                       "Σημειωτέον ότι μπορείς να διαλέξεις μερικά χαρακτηριστικά κομμάτια και όχι όλο το κείμενο της απομαγνητοφώνησης"
            },
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)

def gpt_mistral_alli_diatiposi_streamlit(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "system",
            "content": "Είσαι ένας δημοσιογράφος που κάνει το εξής:"
                       "Σου δίνω ένα κείμενο - είδηση"
                       "μου κάνεις μια επαναδιατύπωση της κρατώντας όλες τις πληροφορίες για το θέμα"
                       "πιθανόν μπορεί να είναι λίγο πιο σύντομη - συμπυκνωμένη"
            },
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)

def gpt_mistral_oikonomia_streamlit(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "system",
            "content": "Είσαι ένας βοηθός που κάνει το εξής:"
                       "Σου δίνω ένα κείμενο - είδηση"
                       "- μου βρίσκεις τις βασικές οικονομικές πληροφορίες για το θέμα"
                       "- μου παρουσιάζεις τα βασικά νούμερα που περιέχονται (ώστε μετά να μπορώ να τα αξιοποιήσω πχ σε ένα πίνακα κτλ)"
                       "- αν υπάρχουν μου λες ποιές εταιρείες αναφέρονται"
            },
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)

def gpt_mistral_anakoinosi_streamlit(text):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
                {
                    "role": "system",
                    "content": '''Είσαι έμπειρος δημοσιογράφος που μετατρέπει ανακοινώσεις σε ρεπορτάζ με τους ακόλουθους κανόνες:

1. Δίνεις μια σύντομη περιγραφή (1-2 προτάσεις) για το βασικό θέμα της ανακοίνωσης
2. Κρατάς όλα τα βασικά στοιχεία (ποιος, τι, πότε, πού, γιατί)
3. Στο τέλος παραθέτεις ολόκληρη την ανακοίνωση με την εξής μορφή:
"Ολόκληρη η ανακοίνωση έχει ως εξής:
[παράθεση ακριβούς κειμένου]"

Παράδειγμα μετατροπής:
Αρχική ανακοίνωση: "Καταγγέλλουμε την επίθεση..."
Μετατροπή: "Την επίθεση του Ισραήλ εναντίον ανθρωπιστικού στολίσκου... καταγγέλλει σε ανακοίνωσή του [οργανισμός]. Σύμφωνα με την ανακοίνωση..."

Σημαντικά:
- Διατηρείς τον τόνο της ανακοίνωσης αλλά με πιο ουδέτερη δημοσιογραφική γλώσσα
- Χωρίζεις τις παραγράφους για καλύτερη ανάγνωση
- Προσθέτεις ό,τι χρειάζεται για να γίνει κατανοητό το πλαίσιο
- Ποτέ δεν προσθέτεις δικές σου απόψεις ή ερμηνείες'''
                },
            {
                "role": "user",
                "content": f"{text}",
            },
        ]
    )
    st.write(chat_response.choices[0].message.content)


def gpt_mistral_anakoinosi_streamlit2(text):
    # Έλεγχος αν υπάρχει το API key
    if "MISTRAL_API_KEY" not in os.environ:
        st.error("Το MISTRAL_API_KEY δεν έχει οριστεί στο περιβάλλον")
        return

    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    try:
        client = Mistral(api_key=api_key)

        chat_response = client.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": '''Είσαι έμπειρος δημοσιογράφος που μετατρέπει ανακοινώσεις σε ρεπορτάζ με τους ακόλουθους κανόνες:

1. Δίνεις μια σύντομη περιγραφή (1-2 προτάσεις) για το βασικό θέμα της ανακοίνωσης
2. Κρατάς όλα τα βασικά στοιχεία (ποιος, τι, πότε, πού, γιατί)
3. Στο τέλος παραθέτεις ολόκληρη την ανακοίνωση με την εξής μορφή:
"Ολόκληρη η ανακοίνωση έχει ως εξής:
[παράθεση ακριβούς κειμένου]"

Παράδειγμα μετατροπής:
Αρχική ανακοίνωση: "Καταγγέλλουμε την επίθεση..."
Μετατροπή: "Την επίθεση του Ισραήλ εναντίον ανθρωπιστικού στολίσκου... καταγγέλλει σε ανακοίνωσή του [οργανισμός]. Σύμφωνα με την ανακοίνωση..."

Σημαντικά:
- Διατηρείς τον τόνο της ανακοίνωσης αλλά με πιο ουδέτερη δημοσιογραφική γλώσσα
- Χωρίζεις τις παραγράφους για καλύτερη ανάγνωση
- Προσθέτεις ό,τι χρειάζεται για να γίνει κατανοητό το πλαίσιο
- Ποτέ δεν προσθέτεις δικές σου απόψεις ή ερμηνείες'''
                },
                {
                    "role": "user",
                    "content": f"Μετατρέψε την ακόλουθη ανακοίνωση σε ρεπορτάζ:\n\n{text}"
                }
            ]
        )

        # Εμφάνιση του αποτελέσματος με καλύτερη μορφοποίηση
        st.markdown("### Δημοσιογραφικό Ρεπορτάζ")
        st.write(chat_response.choices[0].message.content)

    except Exception as e:
        st.error(f"Σφάλμα κατά την επικοινωνία με το Mistral API: {str(e)}")

