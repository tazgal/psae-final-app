import pandas as pd
import streamlit as st
import os
import datetime
import plotly.express as px  


def pandas_show_df(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        st.write("📊 Περιεχόμενο αρχείου (επεξεργάσιμα):")

        edited_df = st.data_editor(
        df,
        num_rows="dynamic",  # 🔑 επιτρέπει προσθήκη / διαγραφή γραμμών
        )

    else:
        st.info("⏳ Παρακαλώ ανέβασε ένα αρχείο .xlsx")



def str_add_to_df(CSV_FILE):    
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Ημερομηνία", "Πολιτική", "Οικονομία ", "Διεθνής οικονομία", "Γεωστρατηγικά", "Εμπλοκή", "Osint"])

    with st.form("my_agenda_form"):
        date = st.date_input("enter date", datetime.date.today())
        politics = st.text_area("Πολιτική")
        economy = st.text_area("Οικονομία")
        int_economy = st.text_area("Διεθνής Οικονομία")
        geopolitics = st.text_area("Γεωστρατηγικά")
        emploki = st.text_area("Εμπλοκή")
        osint = st.text_area("Osint")

        submitted = st.form_submit_button("Αποθήκευση")

    if submitted:
        new_row = {
            "Ημερομηνία": date,
            "Πολιτική": politics,
            "Οικονομία": economy,
            "Διεθνής οικονομία": int_economy,
            "Γεωστρατηγικά": geopolitics,
            "Εμπλοκή": emploki,
            "Osint": osint
    
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Αποθήκευση σε CSV
        df.to_csv(CSV_FILE, index=False)

        st.success("Τα δεδομένα αποθηκεύτηκαν!")

def show_csv(csv_file):
    """
    Φορτώνει CSV και το εμφανίζει ως read-only dataframe
    """
    if not os.path.exists(csv_file):
        st.warning("Το αρχείο CSV δεν βρέθηκε.")
        return None

    df = pd.read_csv(csv_file)
    st.dataframe(df, use_container_width=True)

    return df

def edit_csv(csv_file):
    """
    Εμφανίζει editable dataframe και αποθηκεύει αλλαγές στο CSV
    """
    if not os.path.exists(csv_file):
        st.warning("Το αρχείο CSV δεν βρέθηκε.")
        return None

    df = pd.read_csv(csv_file)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"editor_{csv_file}"
    )

    if st.button("💾 Αποθήκευση αλλαγών"):
        edited_df.to_csv(csv_file, index=False)
        st.success("Το CSV ενημερώθηκε!")

    return edited_df

def show_csv_interactive(csv_file):
    """
    Φορτώνει CSV και εμφανίζει διαδραστικά το DataFrame.
    Μπορείς να κάνεις toggle κανονική / αντιμεταστραμμένη προβολή.
    """
    if not os.path.exists(csv_file):
        st.warning("Το αρχείο CSV δεν βρέθηκε.")
        return None

    # Φόρτωσε CSV μία φορά
    df = pd.read_csv(csv_file)

    # Δημιουργία session_state για toggle
    if "transpose_view" not in st.session_state:
        st.session_state["transpose_view"] = False

    # Κουμπί toggle
    if st.button("Toggle transpose view"):
        st.session_state["transpose_view"] = not st.session_state["transpose_view"]

    # Εμφάνιση ανάλογα με το toggle
    if st.session_state["transpose_view"]:
        st.subheader("Transposed View")
        st.dataframe(df.T, use_container_width=True)
    else:
        st.subheader("Normal View")
        st.dataframe(df, use_container_width=True)

    return df

def dataframe_explorer(
    folder: str,
):

    # ---------- LOAD DATA ----------
    files = [f for f in os.listdir(folder) if f.lower().endswith((".csv", ".xlsx", ".xls"))]

    source = st.radio(
        "Data Source",
        ["📂 My files", "⬆ Upload file"],
        horizontal=True
    )

    df = None

    if source == "📂 My files":
        if not files:
            st.warning("Δεν βρέθηκαν CSV/Excel στον φάκελο")
            return

        selected = st.selectbox("Choose CSV/Excel", files)
        path = os.path.join(folder, selected)
        if selected.lower().endswith(".csv"):
            df = pd.read_csv(path)
        elif selected.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(path)

    else:
        uploaded = st.file_uploader(
            "Ανέβασε CSV ή Excel",
            type=["csv", "xlsx"]
        )

        if uploaded:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)

    if df is None:
        return

    # ---------- EDIT DATA ----------
    st.subheader("✏️ Change data")

    df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor"
    )

    # ---------- CHART BUILDER ----------
    st.subheader("📈 Create chart")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    all_cols = df.columns.tolist()

    chart_type = st.selectbox(
        "Τύπος γραφήματος",
        ["Bar", "Line", "Scatter", "Pie"]
    )

    x_col = st.selectbox("Στήλη X", all_cols)

    y_col = None
    if chart_type != "Pie":
        y_col = st.selectbox("Στήλη Y", numeric_cols)

    color_col = st.selectbox(
        "Χρώμα (προαιρετικό)",
        ["—"] + all_cols
    )

    # ---------- BUILD PLOT ----------
    fig = None

    if chart_type == "Bar":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=None if color_col == "—" else color_col,
            text=y_col
        )

        fig.update_traces(
        textposition="outside",   # πάνω από τις μπάρες
        texttemplate="%{text}"    # format τιμής (προαιρετικό)
        )

    elif chart_type == "Line":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=None if color_col == "—" else color_col
        )

    elif chart_type == "Scatter":
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=None if color_col == "—" else color_col
        )

    elif chart_type == "Pie":
        fig = px.pie(
            df,
            names=x_col,
            values=y_col or numeric_cols[0]
        )

    if fig:
        st.plotly_chart(fig, use_container_width=True)

    return df


