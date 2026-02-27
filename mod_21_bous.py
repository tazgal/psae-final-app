import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
import base64

# ---------------- Widgets με μοναδικά keys ----------------
header_date = st.text_input("Πληροφορίες έκδοσης:", key="header_date")
header_text = f"ΗΜΕΡΟΜΗΝΙΑ: {header_date}"

multiselect = st.selectbox(
    "Επέλεξε αριθμό", options=(24, 28, 32, 40, 48), key="num_rows"
)

option = st.radio(
    "Επιλογή δεδομένων:", ["📋 Φτιάξε επιτόπου", "📤 Upload CSV"], key="data_option"
)

def bousoulas_all():
    st.subheader("📊 Ας μπουσουλήσουμε")


    # ---------------- Συνάρτηση για αριθμό γραμμών ----------------
    def number_rows():
        return multiselect

    # ---------------- Συνάρτηση για δημιουργία DataFrame ----------------
    def choose_df():
        num = multiselect
        half = num // 2
        df = pd.DataFrame({
            'Σελ1': list(range(1, half + 1)),
            "K1": [None] * half,
            'ΖΩΝΗ1': [None] * half,
            "Τ1": [None] * half,
            'Σελ2': list(range(num, num - half, -1)),
            "K2": [None] * half,
            'ΖΩΝΗ2': [None] * half,
            "T2": [None] * half
        })
        return df

    # ---------------- Επιλογή δεδομένων ----------------
    if option == "📋 Φτιάξε επιτόπου":
        df = choose_df()
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="edited_df"
        )
    else:
        uploaded_file = st.file_uploader("Φόρτωσε ένα CSV", type=["csv"], key="upload_csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                key="uploaded_df"
            )
        else:
            st.stop()

    rows = number_rows()
    cols = 8
    selected_df = edited_df.iloc[:rows, :cols]

    highlighted_rows = st.multiselect(
        "Επίλεξε ασπρόμαυρες σελίδες:",
        options=list(selected_df.index),
        format_func=lambda x: f"Γραμμή {x + 1}",
        key="highlighted_rows"
    )

    # ---------------- Δημιουργία PDF ----------------
    if st.button("🖨️ Δημιούργησε PDF", key="create_pdf"):
        buffer = io.BytesIO()

        left_margin = right_margin = top_margin = bottom_margin = 20
        page_width, page_height = A4

        available_width = page_width - left_margin - right_margin
        available_height = page_height - top_margin - bottom_margin

        elements = []

        # Προσθήκη επικεφαλίδας
        if header_text:
            styles = getSampleStyleSheet()
            paragraph = Paragraph(header_text, styles["Normal"])
            elements.append(paragraph)
            elements.append(Spacer(1, 12))

        # Διαστάσεις στηλών για 8 στήλες
        col_widths = [
            available_width * 0.05,
            available_width * 0.03,
            available_width * 0.36,
            available_width * 0.06,
            available_width * 0.05,
            available_width * 0.03,
            available_width * 0.36,
            available_width * 0.06
        ]

        actual_rows = len(selected_df)
        max_rows_per_page = 24
        if actual_rows > max_rows_per_page:
            st.warning(f"⚠️ Ο πίνακας έχει {actual_rows} γραμμές και θα χωριστεί σε πολλές σελίδες. Μέγιστο ανά σελίδα: {max_rows_per_page}")
            row_height = (available_height * 0.95) / (max_rows_per_page + 1)
        else:
            row_height = (available_height * 0.95) / (actual_rows + 1)

        # Δημιουργία δεδομένων πίνακα
        table_data = [list(selected_df.columns)] + selected_df.values.tolist()
        total_table_rows = len(table_data)

        # Ανίχνευση και συγχώνευση ίδιων συνεχόμενων τιμών
        span_commands = []
        for col in range(selected_df.shape[1]):
            start_row = None
            last_value = None
            for row in range(selected_df.shape[0]):
                val = selected_df.iat[row, col]
                if val == last_value and val is not None:
                    if start_row is None:
                        start_row = row - 1
                else:
                    if start_row is not None and row - start_row > 1:
                        span_commands.append(('SPAN', (col, start_row + 1), (col, row)))
                    start_row = None
                last_value = val
            if start_row is not None and selected_df.shape[0] - start_row > 1:
                span_commands.append(('SPAN', (col, start_row + 1), (col, selected_df.shape[0])))

        # Καθάρισμα περιεχομένων κάτω κελιών για merged blocks
        for (_, (x1, y1), (x2, y2)) in span_commands:
            for y in range(y1 + 1, y2 + 1):
                table_data[y][x1] = ""

        # Δημιουργία πίνακα
        table = Table(table_data, colWidths=col_widths, rowHeights=[row_height] * total_table_rows)

        # Στυλ πίνακα
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B6EAF")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 11),
            ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (4, 1), (4, -1), 11),

            ('FONTNAME', (2, 1), (2, -1), 'Courier'),
            ('FONTSIZE', (2, 1), (2, -1), 15),
            ('FONTNAME', (6, 1), (6, -1), 'Courier'),
            ('FONTSIZE', (6, 1), (6, -1), 15),
        ])

        # Εφαρμογή SPANs
        for cmd in span_commands:
            style.add(*cmd)

        # Επισήμανση επιλεγμένων γραμμών
        for r in highlighted_rows:
            style.add('BACKGROUND', (0, r + 1), (-1, r + 1), colors.lightgrey)

        # Αφαίρεση εσωτερικών οριζόντιων γραμμών σε merged cells
        for (_, (x1, y1), (x2, y2)) in span_commands:
            for internal_row in range(y1 + 1, y2 + 1):
                style.add('LINEABOVE', (x1, internal_row), (x2, internal_row), 0, colors.white)

        table.setStyle(style)
        elements.append(table)

        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=top_margin,
            bottomMargin=bottom_margin
        )

        pdf.build(elements)
        buffer.seek(0)

        # Εμφάνιση PDF
        base64_pdf = base64.b64encode(buffer.getvalue()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

        st.download_button(
            "📥 Κατέβασε το PDF",
            data=buffer,
            file_name="Μπούσουλας.pdf",
            mime="application/pdf",
            key="download_pdf"
        )

