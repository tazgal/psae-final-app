import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlparse, parse_qs

st.title("Spotify Embed Player σε Streamlit")

# 1️⃣ Εισαγωγή URL από χρήστη
spotify_url = st.text_input("https://open.spotify.com/show/1cPbZJKrFsM84b6rj7XLZl")

if spotify_url:
    try:
        # 2️⃣ Εξαγωγή type και id από το URL
        parsed = urlparse(spotify_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            sp_type, sp_id = path_parts[0], path_parts[1]
            embed_url = f"https://open.spotify.com/embed/{sp_type}/{sp_id}"
            
            # 3️⃣ Εμφάνιση iframe με components.html
            iframe_code = f"""
            <iframe src="{embed_url}" width="100%" height="380" frameborder="0" allow="encrypted-media"></iframe>
            """
            components.html(iframe_code, height=400)
        else:
            st.error("Δεν κατάφερα να εξαγάγω το ID από το URL.")
    except Exception as e:
        st.error(f"Σφάλμα: {e}")

