import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Τίτλος εφαρμογής ---
st.title("Διαμόρφωση Πίνακα & Διάγραμμα")

# --- Δημιουργία / Επεξεργασία Πίνακα ---
st.header("1. Διαμόρφωση Πίνακα")

# Επιλογή τρόπου εισαγωγής δεδομένων
data_source = st.radio(
    "Επιλέξτε τρόπο εισαγωγής δεδομένων:",
    ("Δημιουργία νέου πίνακα", "Ανέβασμα αρχείου CSV/Excel"),
    key="data_source_radio"
)

if data_source == "Δημιουργία νέου πίνακα":
    # Πλήθος γραμμών και στηλών
    rows = st.number_input("Αριθμός γραμμών:", min_value=1, value=5)
    cols = st.number_input("Αριθμός στηλών:", min_value=1, value=3)

    # Δημιουργία κενού DataFrame
    data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            value = st.text_input(f"Γραμμή {i+1}, Στήλη {j+1}:", key=f"cell_{i}_{j}")
            row.append(value)
        data.append(row)

    # Ονόματα στηλών
    column_names = [
        st.text_input(f"Όνομα Στήλης {i+1}:", value=f"Στήλη_{i+1}", key=f"col_name_{i}")
        for i in range(cols)
    ]

    # Δημιουργία DataFrame
    df = pd.DataFrame(data, columns=column_names)

else:
    # Ανέβασμα αρχείου CSV ή Excel
    uploaded_file = st.file_uploader("Επιλέξτε αρχείο CSV/Excel:", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    else:
        st.warning("Παρακαλώ ανεβάστε ένα αρχείο.")
        df = pd.DataFrame()

# Εμφάνιση πίνακα
if not df.empty:
    st.subheader("Προεπισκόπηση Πίνακα")
    st.dataframe(df)

    # Αποθήκευση του πίνακα ως CSV
    st.download_button(
        label="Κατέβασμα ως CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="data.csv",
        mime="text/csv"
    )
else:
    st.warning("Ο πίνακας είναι κενός. Συμπληρώστε δεδομένα.")
    st.stop()  # Σταματάει εδώ αν δεν υπάρχουν δεδομένα

# --- Οπτικοποίηση Δεδομένων ---
st.header("2. Διάγραμμα")

if not df.empty:
    # Επιλογή τύπου διαγράμματος
    chart_type = st.selectbox(
        "Επιλέξτε τύπο διαγράμματος:",
        ["Γραμμή (Line)", "Ραβδογράφημα (Bar)", "Πίτα (Pie)", "Ιστόγραμμα (Histogram)", "Διασπορά (Scatter)"]
    )

    # Επιλογή στηλών για άξονες
    x_axis = st.selectbox("Επιλέξτε στήλη για άξονα X:", df.columns)
    y_axis = st.selectbox("Επιλέξτε στήλη για άξονα Y:", df.columns)

    # Προαιρετικό φιλτράρισμα δεδομένων
    st.subheader("Φίλτρα")
    filter_column = st.selectbox("Επιλέξτε στήλη για φιλτράρισμα (προαιρετικά):", [None] + list(df.columns))
    if filter_column:
        unique_values = df[filter_column].unique()
        selected_values = st.multiselect(f"Επιλέξτε τιμές για τη στήλη '{filter_column}':", unique_values)
        if selected_values:
            df_filtered = df[df[filter_column].isin(selected_values)]
        else:
            df_filtered = df
    else:
        df_filtered = df

    # Δημιουργία διαγράμματος
    st.subheader("Αποτέλεσμα")
    fig, ax = plt.subplots()

    try:
        x_data = pd.to_numeric(df_filtered[x_axis], errors="coerce")
        y_data = pd.to_numeric(df_filtered[y_axis], errors="coerce")

        if chart_type == "Γραμμή (Line)":
            ax.plot(x_data, y_data, marker="o")
            ax.set_title("Διάγραμμα Γραμμής")
        elif chart_type == "Ραβδογράφημα (Bar)":
            ax.bar(x_data, y_data)
            ax.set_title("Ραβδογράφημα")
        elif chart_type == "Πίτα (Pie)":
            ax.pie(y_data, labels=x_data, autopct="%1.1f%%")
            ax.set_title("Διάγραμμα Πίτας")
        elif chart_type == "Ιστόγραμμα (Histogram)":
            ax.hist(y_data, bins=10, edgecolor="black")
            ax.set_title("Ιστόγραμμα")
        elif chart_type == "Διασπορά (Scatter)":
            ax.scatter(x_data, y_data)
            ax.set_title("Διάγραμμα Διασποράς")

        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Σφάλμα κατά τη δημιουργία του διαγράμματος: {e}")
        st.error("Βεβαιωθείτε ότι οι στήλες που επιλέξατε περιέχουν αριθμητικά δεδομένα.")
