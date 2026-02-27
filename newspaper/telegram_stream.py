import streamlit as st
from telegram import Bot

# -----------------------------
# Ρυθμίσεις Bot
# -----------------------------
TOKEN = "ΤΟ_BOT_TOKEN_ΣΟΥ"  # από BotFather
bot = Bot(token=TOKEN)

# -----------------------------
# Sidebar: Στείλε μήνυμα σε χρήστη
# -----------------------------
st.sidebar.header("🔔 Στείλε Ειδήσεις μέσω Telegram Bot")

chat_id = st.sidebar.text_input("Chat ID χρήστη")  # Πρέπει να πάρεις αυτό που ξεκίνησε το bot
message = st.sidebar.text_area("Μήνυμα προς αποστολή")

if st.sidebar.button("Στείλε μήνυμα"):
    if chat_id.strip() and message.strip():
        try:
            bot.send_message(chat_id=chat_id, text=message)
            st.sidebar.success("✅ Μήνυμα σταλεί!")
        except Exception as e:
            st.sidebar.error(f"❌ Σφάλμα: {e}")
    else:
        st.sidebar.warning("Πρέπει να συμπληρώσετε chat_id και μήνυμα.")

# -----------------------------
# Main: Δείξε προηγούμενα μηνύματα ή φόρμα ειδήσεων
# -----------------------------
st.title("📡 Telegram News Sender")
st.write("Στείλε ειδήσεις ή ενημερώσεις στους χρήστες που ξεκίνησαν το bot.")
