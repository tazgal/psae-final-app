import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="📜 Timeline Builder", layout="wide")
st.title("📜 Δημιουργία Timeline")

st.write("""
Αυτό το εργαλείο σου επιτρέπει να δημιουργήσεις ένα **timeline** με γεγονότα, είτε 
ανεβάζοντας ένα CSV είτε εισάγοντας δεδομένα χειροκίνητα.
""")

# --- Ανέβασμα CSV ή χειροκίνητη εισαγωγή ---
uploaded_file = st.file_uploader("📂 Ανέβασε CSV (στήλες: Χρονολογία, Γεγονός, Κατηγορία)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Το CSV ανέβηκε επιτυχώς!")
else:
    st.info("Ή δημιούργησε το δικό σου timeline χειροκίνητα:")
    default_data = pd.DataFrame({
        "Χρονολογία": ["5ος αιώνας π.Χ.", "323 π.Χ.", "146 π.Χ.", "1821", "1974"],
        "Γεγονός": ["Κλασική Εποχή", "Θάνατος Αλεξάνδρου", "Κατάληψη Ελλάδας από Ρώμη", "Επανάσταση", "Αποκατάσταση Δημοκρατίας"],
        "Κατηγορία": ["Αρχαιότητα", "Αρχαιότητα", "Αρχαιότητα", "Νεότερα", "Σύγχρονα"]
    })
    df = st.data_editor(default_data, num_rows="dynamic")

# --- Έλεγχος δεδομένων ---
if df.empty or "Χρονολογία" not in df.columns or "Γεγονός" not in df.columns:
    st.warning("❗ Βεβαιώσου ότι υπάρχουν τουλάχιστον οι στήλες 'Χρονολογία' και 'Γεγονός'.")
    st.stop()

# --- Επιλογή διάταξης ---
layout_choice = st.radio(
    "🧭 Διάταξη timeline:",
    ["Οριζόντια", "Κάθετη"],
    horizontal=True
)

# --- Προσαρμοσμένες ρυθμίσεις βάσει αριθμού καταχωρήσεων ---
num_entries = len(df)
# Προσαρμογή ύψους και αποστάσεων βάσει αριθμού καταχωρήσεων
if num_entries <= 5:
    base_height = 400
    marker_size = 10
    line_length = 0.15  # Μικρότερες αποστάσεις για λίγες καταχωρήσεις
elif num_entries <= 10:
    base_height = 500
    marker_size = 12
    line_length = 0.2
else:
    base_height = 600
    marker_size = 12
    line_length = 0.2

# Προσαρμογή ύψους για κάθετη διάταξη
vertical_height = base_height + (num_entries * 20)

# --- Δημιουργία Timeline ---
st.subheader("🕰️ Οπτικοποίηση Timeline")

# Εναλλάξ πάνω-κάτω (ή δεξιά-αριστερά) για να ξεχωρίζουν τα labels
offsets = [line_length if i % 2 == 0 else -line_length for i in range(len(df))]

fig = go.Figure()

if layout_choice == "Οριζόντια":
    # Γραμμή βάσης
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(df)-0.5,
        y0=0, y1=0,
        line=dict(color="gray", width=2)
    )

    # Συνδέσεις (γραμμές από timeline προς τα labels)
    for i, (x, off) in enumerate(zip(range(len(df)), offsets)):
        fig.add_shape(
            type="line",
            x0=x, x1=x,
            y0=0, y1=off,
            line=dict(color="gray", width=1)
        )

    # Σημεία (γεγονότα) με ημερομηνίες δίπλα στις βούλες
    for i, (x, y, event, date) in enumerate(zip(range(len(df)), offsets, df["Γεγονός"], df["Χρονολογία"])):
        # Προσθήκη βούλας
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers",
            marker=dict(size=marker_size, color="royalblue"),
            showlegend=False,
            hoverinfo="text",
            hovertext=f"<b>{event}</b><br>Χρονολογία: {date}"
        ))
        
        # Προσθήκη κειμένου με ημερομηνία
        fig.add_annotation(
            x=x, y=y,
            text=f"<b>{date}</b><br>{event}",
            showarrow=False,
            yshift=35 if y > 0 else -35,  # Αυξημένη απόσταση
            xanchor="center",
            align="center",
            font=dict(size=11)
        )

    # Άξονες
    fig.update_layout(
        xaxis=dict(
            showticklabels=False,
            showgrid=False, showline=False, zeroline=False,
        ),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        height=base_height,
        title="Οριζόντιο Timeline"
    )

else:
    # Κάθετο timeline
    fig.add_shape(
        type="line",
        x0=0, x1=0,
        y0=-0.5, y1=len(df)-0.5,
        line=dict(color="gray", width=2)
    )

    # Κοινή απόσταση για ΟΛΑ (γραμμές, βούλες, κείμενο)
    short_offsets = [off * 0.2 for off in offsets]  # Μόνο ΕΔΩ γίνεται η μείωση!

    # Συνδέσεις (γραμμές) και βούλες με τις ΚΟΙΝΕΣ μικρές θέσεις
    for i, (y, off) in enumerate(zip(range(len(df)), short_offsets)):
        event = df["Γεγονός"].iloc[i]
        date = df["Χρονολογία"].iloc[i]
        
        # Γραμμή σύνδεσης - ΧΡΗΣΙΜΟΠΟΙΕΙ ΤΟ off (που είναι ΗΔΗ μειωμένο)
        fig.add_shape(
            type="line",
            x0=0, x1=off,  # ΧΩΡΙΣ επιπλέον πολλαπλασιασμό
            y0=y, y1=y,
            line=dict(color="gray", width=1)
        )
        
        # Προσθήκη βούλας - ΧΡΗΣΙΜΟΠΟΙΕΙ ΤΟ off (που είναι ΗΔΗ μειωμένο)
        fig.add_trace(go.Scatter(
            x=[off], y=[y],
            mode="markers",
            marker=dict(size=marker_size, color="royalblue"),
            showlegend=False,
            hoverinfo="text",
            hovertext=f"<b>{event}</b><br>Χρονολογία: {date}"
        ))
        
        # Προσθήκη κειμένου με ημερομηνία - ΧΡΗΣΙΜΟΠΟΙΕΙ ΤΟ off (που είναι ΗΔΗ μειωμένο)
        fig.add_annotation(
            x=off, y=y,
            text=f"<b>{date}</b><br>{event}",
            showarrow=False,
            xshift=45 if off > 0 else -45,
            yanchor="middle",
            align="left" if off > 0 else "right",
            font=dict(size=11)
        )

    # Άξονες
    fig.update_layout(
        yaxis=dict(
            showticklabels=False,
            autorange="reversed",
            showgrid=False, showline=False, zeroline=False
        ),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        height=vertical_height,
        title="Κάθετο Timeline"
    )

# Κοινές ρυθμίσεις για και τις δύο διατάξεις
fig.update_layout(
    showlegend=False,
    margin=dict(l=40, r=40, t=80, b=40),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# --- Εξαγωγή CSV ---
csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="💾 Κατέβασε τα δεδομένα (CSV)",
    data=csv_bytes,
    file_name="timeline.csv",
    mime="text/csv"
)