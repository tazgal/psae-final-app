import os
import base64
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Gmail scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.send"]

def gmail_authenticate():
    creds = None
    token_path = "token.json"

    if os.path.exists(token_path):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def get_emails(service, max_results=5):
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(Χωρίς θέμα)")
        snippet = msg_data.get("snippet", "")
        emails.append({"subject": subject, "snippet": snippet})
    return emails


def send_email(service, to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}
    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    return send_message


# Streamlit UI
st.title("📧 Gmail App")

if "service" not in st.session_state:
    st.session_state.service = gmail_authenticate()

service = st.session_state.service

menu = st.sidebar.radio("Επιλογή", ["Δες emails", "Στείλε email"])

if menu == "Δες emails":
    emails = get_emails(service)
    for e in emails:
        st.subheader(e["subject"])
        st.write(e["snippet"])
        st.write("---")

elif menu == "Στείλε email":
    to = st.text_input("Παραλήπτης:")
    subject = st.text_input("Θέμα:")
    msg = st.text_area("Μήνυμα:")
    if st.button("Αποστολή"):
        send_email(service, to, subject, msg)
        st.success("✅ Το email εστάλη!")
