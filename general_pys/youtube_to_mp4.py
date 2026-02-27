import streamlit as st
import yt_dlp
import os

# Ρύθμιση σελίδας
st.set_page_config(page_title="YouTube to MP4 Downloader", page_icon="🎬")
st.title("🎬 YouTube Video Downloader")
st.write("Μετατροπή βίντεο YouTube σε MP4 (προσωπική χρήση).")

# Εισαγωγή URL
url = st.text_input("Επικόλλησε εδώ το URL του βίντεο YouTube:")

if url:
    try:
        # Λήψη πληροφοριών βίντεο
        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            thumbnail_url = info['thumbnail']
            duration = info['duration']

            # Εμφάνιση πληροφοριών
            st.subheader(f"📺 Τίτλος: {title}")
            st.image(thumbnail_url, width=400)
            st.write(f"**Διάρκεια:** {duration // 60} λεπτά και {duration % 60} δευτερόλεπτα")

        # Επιλογή ποιότητας
        formats = yt_dlp.YoutubeDL({'listformats': True, 'quiet': True}).extract_info(url, download=False)['formats']
        mp4_formats = [f for f in formats if f.get('ext') == 'mp4' and f.get('height')]
        format_options = {f"{f['format_id']}: {f['height']}p" for f in mp4_formats}
        selected_format = st.selectbox("Επιλογή ποιότητας:", format_options)

        # Φάκελος αποθήκευσης
        output_path = st.text_input("Φάκελος αποθήκευσης (π.χ. 'downloads/'):", "downloads/")
        os.makedirs(output_path, exist_ok=True)

        # Λήψη βίντεο
        if st.button("Λήψη βίντεο"):
            format_id = selected_format.split(":")[0]
            ydl_opts_download = {
                'format': format_id,
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            with st.spinner("Λήψη σε εξέλιξη..."):
                with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                    ydl.download([url])
                st.success(f"✅ Το βίντεο αποθηκεύτηκε στο φάκελο '{output_path}'!")

    except Exception as e:
        st.error(f"⚠️ Σφάλμα: {e}")
