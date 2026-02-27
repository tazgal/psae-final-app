import streamlit as st

st.sidebar.title("📚 Μενού")

with st.sidebar.expander("📁 Εικόνες"):
    st.write("🖼️ Εμφάνιση εικόνων")
    st.write("🔍 Αναζήτηση")

with st.sidebar.expander("📊 Διαγράμματα"):
    st.write("📈 Γραφήματα")
    st.write("📉 Αναλύσεις")

with st.sidebar.expander("⚙️ Ρυθμίσεις"):
    st.write("🧩 Επιλογές")
    st.write("🧹 Καθαρισμός cache")