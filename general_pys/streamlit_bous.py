import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
import base64

st.subheader("📊 Ας μπουσουλήσουμε")

header_date = st.text_input("Ημερομηνία έκδοσης:")
header_text = f"ΗΜΕΡΟΜΗΝΙΑ: {header_date}"

multiselect = st.selectbox("Επέλεξε αριθμό", options=(24, 28, 32, 40))

# Συνάρτηση για δημιουργία DataFrame
def choose_df():
    num = multiselect
    half = num // 2
    df = pd.DataFrame({
        'Σελ1': list(range(1, half + 1)),
        'ΥΛΗ1': [None] * half,
        'Σελ2': list(range(num, num - half, -1)),
        'ΥΛΗ2': [None] * half
    })
    return df

# Επιλογή: είτε sample data είτε upload
option = st.radio("Επιλογή δεδομένων:", ["📋 Φτιάξε επιτόπου", "📤 Upload CSV"])

if option == "📋 Φτιάξε επιτόπου":
    df = choose_df()
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="edited1"
    )
else:
    uploaded_file = st.file_uploader("Φόρτωσε ένα CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="uploaded")
    else:
        st.stop()

rows = st.number_input("Αριθμός γραμμών", 1, len(edited_df), value=min(12, len(edited_df)))
cols = 4
selected_df = edited_df.iloc[:rows, :cols]

if st.button("🖨️ Δημιούργησε PDF"):
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

    # Διαστάσεις στηλών
    if cols == 4:
        col_widths = [
            available_width * 0.05,
            available_width * 0.45,
            available_width * 0.05,
            available_width * 0.45,
        ]
    else:
        col_widths = [available_width / cols] * cols

    max_rows_per_page = 20
    if rows > max_rows_per_page:
        st.warning(f"⚠️ Ο πίνακας έχει {rows} γραμμές και θα χωριστεί σε πολλές σελίδες. Μέγιστο ανά σελίδα: {max_rows_per_page}")
        row_height = (available_height * 0.95) / (max_rows_per_page + 1)
    else:
        row_height = (available_height * 0.95) / (rows + 1)

    # Δημιουργία δεδομένων πίνακα
    table_data = [list(selected_df.columns)] + selected_df.values.tolist()

    # --- 🔁 Ανίχνευση ίδιων συνεχόμενων τιμών και συγχώνευση (SPAN)
    span_commands = []
    for col in range(selected_df.shape[1]):
        start_row = None
        last_value = None
        for row in range(selected_df.shape[0]):
            val = selected_df.iat[row, col]
            if val == last_value and val is not None:
                # Συνέχεια ίδιου value
                if start_row is None:
                    start_row = row - 1
            else:
                # Αν κλείνει μια σειρά ίδιων τιμών
                if start_row is not None and row - start_row > 1:
                    span_commands.append(('SPAN', (col, start_row + 1), (col, row)))
                start_row = None
            last_value = val
        # Τελευταίο group στο τέλος
        if start_row is not None and selected_df.shape[0] - start_row > 1:
            span_commands.append(('SPAN', (col, start_row + 1), (col, selected_df.shape[0])))

    # Καθάρισε τα περιεχόμενα των κάτω κελιών στα merged blocks
    for (_, (x1, y1), (x2, y2)) in span_commands:
        for y in range(y1 + 1, y2 + 1):
            table_data[y][x1] = ""

    # Δημιουργία πίνακα
    table = Table(table_data, colWidths=col_widths, rowHeights=[row_height]*(rows+1))

    # Στυλ πίνακα
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B6EAF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ])

    # Εφαρμογή SPANs
    for cmd in span_commands:
        style.add(*cmd)

    # ΔΙΟΡΘΩΜΕΝΟ: Σβήσε ΜΟΝΟ τις εσωτερικές οριζόντιες γραμμές
    for (_, (x1, y1), (x2, y2)) in span_commands:
        # Αφαίρεση εσωτερικών οριζόντιων γραμμών (LINEABOVE για όλες τις εσωτερικές γραμμές)
        for internal_row in range(y1 + 1, y2 + 1):
            style.add('LINEABOVE', (x1, internal_row), (x2, internal_row), 0, colors.white)
        
        # ΔΙΑΤΗΡΗΣΗ των εξωτερικών γραμμών:
        # - LINEBEFORE (αριστερά) παραμένει
        # - LINEAFTER (δεξιά) παραμένει  
        # - LINEBELOW (κάτω) παραμένει
        # - LINEABOVE (πάνω) παραμένει

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
        mime="application/pdf"
    )