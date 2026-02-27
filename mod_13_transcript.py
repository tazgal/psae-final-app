from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import streamlit as st
import whisper
import tempfile

def transcribe_youtube():
    # Παίρνουμε URL από τον χρήστη
    url = input("Please enter YouTube URL: ")

    # Ανάλυση URL για να πάρουμε το video_id
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        video_id = video_id[0]  # παίρνουμε το πρώτο αποτέλεσμα
    else:
        raise ValueError("Δεν βρέθηκε video_id στο URL")

    # Κλήση στο API
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=['el','en'])

    # Προσπέλαση με attributes
    full_text = "\n".join([item.text for item in transcript])
    print(full_text)

def transcribe_youtube_streamlit(url):
    # Παίρνουμε URL από τον χρήστη

    # Ανάλυση URL για να πάρουμε το video_id
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        video_id = video_id[0]  # παίρνουμε το πρώτο αποτέλεσμα
    else:
        raise ValueError("Δεν βρέθηκε video_id στο URL")

    # Κλήση στο API
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=['el','en'])

    # Προσπέλαση με attributes
    full_text = "\n".join([item.text for item in transcript])
    st.write(full_text)

def transcribe_mp3_whisper():
    model = whisper.load_model("base")  # ή tiny/small/medium/large
    result = model.transcribe("sound_test.mp3", language="el")
    print(result["text"])


def transcribe_mp3_streamlit():
    st.title("Απομαγνητοφώνηση MP3 με Whisper")

    # Βήμα 1: Ο χρήστης ανεβάζει το αρχείο
    uploaded_file = st.file_uploader(
        "Επέλεξε ένα αρχείο MP3 για απομαγνητοφώνηση",
        type=["mp3"]
    )

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/mp3")  # Προαιρετικά: αναπαραγωγή στο UI

        # Βήμα 2: Αποθήκευση προσωρινά σε αρχείο γιατί το Whisper θέλει path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        # Βήμα 3: Φόρτωση μοντέλου Whisper (π.χ. small για γρηγορότερο)
        model = whisper.load_model("small")

        # Βήμα 4: Απομαγνητοφώνηση
        result = model.transcribe(temp_path, language="el")

        # Βήμα 5: Εμφάνιση κειμένου
        st.subheader("Απομαγνητοφώνηση")
        st.write(result["text"])


def transcribe_mp3_streamlit2(uploaded_file):

    if uploaded_file is not None:
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        model = whisper.load_model("medium")
        result = model.transcribe(temp_path, language="el")

        st.subheader("Απομαγνητοφώνηση")
        st.write(result["text"])