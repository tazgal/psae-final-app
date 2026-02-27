import os
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu


CSV_FILE = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/images/images.csv"  # CSV με tags & τίτλους
IMAGE_FOLDER = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/images"     # Φάκελος με εικόνες


@st.cache_data
def load_csv(csv_file):
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    return pd.DataFrame()  # Άδειο αν δεν υπάρχει

def search_images2():
    
    CSV_FILE = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/images/images.csv"  # CSV με tags & τίτλους
    IMAGE_FOLDER = "/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/images"
    
    df = load_csv(CSV_FILE)

    # --- Αρχικοποίηση session_state ---
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "selected_csv_image" not in st.session_state:
        st.session_state.selected_csv_image = None
    if "selected_folder_image" not in st.session_state:
        st.session_state.selected_folder_image = None

    files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]


    images_menu = option_menu(
        "Αναζήτηση εικόνες και διαγράμματα",
        ["Αναζήτηση σε CSV", "Επιλογή με όνομα αρχείου", "Ολες οι εικόνες","Επεξεργασία CSV"]
    )

    if images_menu == "Αναζήτηση σε CSV":  
        st.subheader("Ψάξε με CSV")

        # --- Αναζήτηση ---
        query = st.text_input(
            "Αναζήτηση (tags ή τίτλος):", 
            value=st.session_state.search_query, 
            key="search_csv_input"
        )
        st.session_state.search_query = query

        if not df.empty:
            if query:
                filtered_df = df[df.apply(
                    lambda row: query.lower() in str(row['tags']).lower() 
                                or query.lower() in str(row['title']).lower(), axis=1)]
            else:
                filtered_df = df

            if filtered_df.empty:
                st.warning("Δεν βρέθηκαν εικόνες που ταιριάζουν στην αναζήτηση!")
            else:
                st.write("Επιλογή εικόνας από τα αποτελέσματα αναζήτησης:")
                default_index = 0
                if st.session_state.selected_csv_image in filtered_df['filename'].tolist():
                    default_index = filtered_df['filename'].tolist().index(st.session_state.selected_csv_image)

                st.session_state.selected_csv_image = st.selectbox(
                    "Επίλεξε εικόνα:", 
                    filtered_df['filename'], 
                    index=default_index,
                    key="select_csv"
                )

                # Εμφάνιση επιλεγμένης εικόνας
                image_path = os.path.join(IMAGE_FOLDER, st.session_state.selected_csv_image)
                if os.path.exists(image_path):
                    st.image(Image.open(image_path), caption=st.session_state.selected_csv_image, use_container_width=True)
                else:
                    st.error("Η εικόνα δεν βρέθηκε στον φάκελο!")

                st.write("Όλες οι εικόνες που ταιριάζουν στην αναζήτηση:")
                cols = st.columns(3)
                for i, file in enumerate(filtered_df['filename']):
                    with cols[i % 3]:
                        img_path = os.path.join(IMAGE_FOLDER, file)
                        if os.path.exists(img_path):
                            st.image(Image.open(img_path), caption=file, use_container_width=True)
        else:
            st.error("Δεν βρέθηκε το CSV με τα metadata!")


    elif images_menu == "Επιλογή με όνομα αρχείου":
    
        st.subheader("Επιλογή εικόνας με όνομα από φάκελο")

        if files:
            default_index = 0
            if st.session_state.selected_folder_image in files:
                default_index = files.index(st.session_state.selected_folder_image)

            st.session_state.selected_folder_image = st.selectbox(
                "Επίλεξε εικόνα:", 
                files, 
                index=default_index,
                key="select_folder"
            )

            image_path = os.path.join(IMAGE_FOLDER, st.session_state.selected_folder_image)
            st.image(Image.open(image_path), caption=st.session_state.selected_folder_image, use_container_width=True)
        else:
            st.warning("Δεν υπάρχουν εικόνες στο φάκελο!")

    elif images_menu == ("Ολες οι εικόνες"):
        # --- Εμφάνιση όλων των εικόνων ---
        st.subheader("Όλες οι εικόνες")
        if files:
            cols = st.columns(3)
            for i, file in enumerate(files):
                with cols[i % 3]:
                    st.image(Image.open(os.path.join(IMAGE_FOLDER, file)), caption=file, use_container_width=True)

    elif images_menu == ("Επεξεργασία CSV"):

        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="csv_editor"
        )

        # Κουμπί αποθήκευσης
        if st.button("💾 Αποθήκευση Αλλαγών", key="save_csv"):
            try:
                edited_df.to_csv(CSV_FILE, index=False)
                st.cache_data.clear()
                st.session_state["csv_saved"] = True  # αποθηκεύουμε flag στο session
            except Exception as e:
                st.error(f"Σφάλμα κατά την αποθήκευση: {e}")

        if files:
            cols = st.columns(3)
            for i, file in enumerate(files):
                with cols[i % 3]:
                    st.image(Image.open(os.path.join(IMAGE_FOLDER, file)), caption=file, use_container_width=True)
       


