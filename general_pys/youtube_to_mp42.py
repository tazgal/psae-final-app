
import streamlit as st
import yt_dlp
import os
from pathlib import Path
import subprocess


# Ρύθμιση σελίδας
st.set_page_config(page_title="YouTube to MP4 Downloader", page_icon="🎬")
st.title("🎬 YouTube Video Downloader")
st.write("Μετατροπή βίντεο YouTube σε MP4 (μόνο για προσωπική χρήση).")

# Εισαγωγή URL
url = st.text_input("Επικόλλησε εδώ το URL του βίντεο YouTube:")

if url:
    try:
        # Πληροφορίες βίντεο
        ydl_opts_info = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get('title', 'video')
        thumbnail_url = info.get('thumbnail', '')
        duration = info.get('duration', 0)

        # Εμφάνιση πληροφοριών
        st.subheader(f"📺 Τίτλος: {title}")
        if thumbnail_url:
            st.image(thumbnail_url, width=400)
        st.write(f"**Διάρκεια:** {duration // 60} λεπτά και {duration % 60} δευτερόλεπτα")

        # Επιλογή ποιότητας
        mp4_formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('height')]
        format_options = [f"{f['format_id']}: {f['height']}p" for f in mp4_formats]
        selected_format = st.selectbox("Επιλογή ποιότητας:", format_options)

        # Φάκελος αποθήκευσης
        output_path = st.text_input("Φάκελος αποθήκευσης (π.χ. 'downloads/'):", "downloads/")
        os.makedirs(output_path, exist_ok=True)

        # Λήψη
        if st.button("Λήψη βίντεο"):
            format_id = selected_format.split(":")[0]
            safe_title = "".join(c for c in title if c.isalnum() or c in " _-").rstrip()
            ydl_opts_download = {
                'format': f'{format_id}+bestaudio/best',
                'outtmpl': f'{output_path}/{safe_title}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }],
            }
            with st.spinner("⏳ Λήψη σε εξέλιξη..."):
                with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                    ydl.download([url])
            st.success(f"✅ Το βίντεο αποθηκεύτηκε στο φάκελο '{output_path}'!")


    except Exception as e:
        st.error(f"⚠️ Σφάλμα: {e}")

if st.button("📂 Άνοιγμα φακέλου"):
    subprocess.run(["open", output_path])