import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from mod_01_enter_open import *

def horizontal_timeline_app():

    st.set_page_config(page_title="Timeline Builder", layout="wide")

    dataframe_explorer3("data/csvs","timeline")


    st.info("paste here or create manually")
    df = pd.DataFrame({
        "Χρονολογία": [""],
        "Γεγονός": [
            ""
        ]
    })

    # =========================
    # ✏️ Επεξεργασία δεδομένων
    # =========================
    df = st.data_editor(df, num_rows="dynamic")

    if df.empty or not {"Χρονολογία", "Γεγονός"}.issubset(df.columns):
        st.warning("❗ Απαιτούνται οι στήλες: Χρονολογία, Γεγονός")
        st.stop()

    # =========================
    # 🔗 Group by ημερομηνία
    # =========================
    grouped = (
        df
        .groupby("Χρονολογία", sort=False)["Γεγονός"]
        .apply(list)
        .reset_index()
    )

    def format_events(events):
        return "<br>".join([f"• {e}" for e in events])

    num_entries = len(grouped)

    # =========================
    # 📐 Προσαρμογή layout
    # =========================
    if num_entries <= 5:
        height, marker_size, line_length = 400, 10, 0.15
    elif num_entries <= 10:
        height, marker_size, line_length = 500, 12, 0.2
    else:
        height, marker_size, line_length = 600, 12, 0.2

    offsets = [line_length if i % 2 == 0 else -line_length for i in range(num_entries)]

    # =========================
    # 🕰️ Timeline
    # =========================
    fig = go.Figure()

    # Κεντρική γραμμή
    fig.add_shape(
        type="line",
        x0=-0.5, x1=num_entries - 0.5,
        y0=0, y1=0,
        line=dict(color="gray", width=2)
    )

    for i, off in enumerate(offsets):
        date = grouped["Χρονολογία"][i]
        events = grouped["Γεγονός"][i]

        # Γραμμή σύνδεσης
        fig.add_shape(
            type="line",
            x0=i, x1=i,
            y0=0, y1=off,
            line=dict(color="gray", width=1)
        )

        # Bullet
        fig.add_trace(go.Scatter(
            x=[i], y=[off],
            mode="markers",
            marker=dict(size=marker_size, color="royalblue"),
            hoverinfo="text",
            hovertext=f"<b>{date}</b><br>" + "<br>".join(events),
            showlegend=False
        ))

        # Annotation
        fig.add_annotation(
            x=i, y=off,
            text=f"<b>{date}</b><br>{format_events(events)}",
            showarrow=False,
            yshift=40 if off > 0 else -40,
            align="left",
            font=dict(size=11)
        )

    fig.update_layout(
        height=height,
        title="Timeline",
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 💾 Export
    # =========================
    st.download_button(
        "💾 Κατέβασε CSV",
        df.to_csv(index=False).encode("utf-8"),
        "timeline.csv",
        "text/csv"
    )





def estimate_text_height(events, base=40, per_line=14):
    return base + per_line * len(events)


def horizontal_timeline_app2():

    st.set_page_config(page_title="Timeline Builder", layout="wide")

    dataframe_explorer3("data/csvs","timeline")


    st.info("paste here or create manually")
    df = pd.DataFrame({
        "Χρονολογία": [""],
        "Γεγονός": [
            ""
        ]
    })

    # =========================
    # ✏️ Επεξεργασία δεδομένων
    # =========================
    df = st.data_editor(df, num_rows="dynamic")

    if df.empty or not {"Χρονολογία", "Γεγονός"}.issubset(df.columns):
        st.warning("❗ Απαιτούνται οι στήλες: Χρονολογία, Γεγονός")
        st.stop()

    # =========================
    # 🔗 Group by ημερομηνία
    # =========================
    grouped = (
        df
        .groupby("Χρονολογία", sort=False)["Γεγονός"]
        .apply(list)
        .reset_index()
    )

    def format_events(events):
        return "<br>".join([f"• {e}" for e in events])

    num_entries = len(grouped)

    # =========================
    # 📐 Προσαρμογή layout
    # =========================
    if num_entries <= 5:
        height, marker_size, line_length = 400, 10, 0.15
    elif num_entries <= 10:
        height, marker_size, line_length = 500, 12, 0.2
    else:
        height, marker_size, line_length = 600, 12, 0.2

    offsets = [line_length if i % 2 == 0 else -line_length for i in range(num_entries)]

    # =========================
    # 🕰️ Timeline
    # =========================
    fig = go.Figure()

    # Κεντρική γραμμή
    fig.add_shape(
        type="line",
        x0=-0.5, x1=num_entries - 0.5,
        y0=0, y1=0,
        line=dict(color="gray", width=2)
    )

    for i, off in enumerate(offsets):
        date = grouped["Χρονολογία"][i]
        events = grouped["Γεγονός"][i]

        # Γραμμή σύνδεσης
        fig.add_shape(
            type="line",
            x0=i, x1=i,
            y0=0, y1=off,
            line=dict(color="gray", width=1)
        )

        # Bullet
        fig.add_trace(go.Scatter(
            x=[i], y=[off],
            mode="markers",
            marker=dict(size=marker_size, color="royalblue"),
            hoverinfo="text",
            hovertext=f"<b>{date}</b><br>" + "<br>".join(events),
            showlegend=False
        ))

        text_height = estimate_text_height(events)

        # Annotation
        fig.add_annotation(
            x=i,
            y=off,
            text=f"<b>{date}</b><br>{format_events(events)}",
            showarrow=False,
            yshift=text_height if off > 0 else -text_height,
            align="left",
            font=dict(size=11)
        )

    fig.update_layout(
        height=height,
        title="Timeline",
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 💾 Export
    # =========================
    st.download_button(
        "💾 Κατέβασε CSV",
        df.to_csv(index=False).encode("utf-8"),
        "timeline.csv",
        "text/csv"
    )

def horizontal_timeline_app3():

    st.set_page_config(page_title="Timeline Builder", layout="wide")

    dataframe_explorer3("data/csvs", "timeline")

    # 🔁 NEW: επιλογή layout
    layout_mode = st.radio(
        "Layout",
        ["Horizontal", "Vertical"],
        horizontal=True,
        key="timeline_layout_mode"
    )

    st.info("paste here or create manually")
    df = pd.DataFrame({
        "Date": [""],
        "Event": [""]
    })

    df = st.data_editor(df, num_rows="dynamic")

    if df.empty or not {"Date", "Event"}.issubset(df.columns):
        st.warning("Cols Date, Event required")
        st.stop()

    grouped = (
        df
        .groupby("Date", sort=False)["Event"]
        .apply(list)
        .reset_index()
    )

    def format_events(events):
        return "<br>".join([f"• {e}" for e in events])

    def estimate_text_height(events, base=40, per_line=14):
        return base + per_line * len(events)

    num_entries = len(grouped)

    # =========================
    # 📐 Προσαρμογή layout
    # =========================
    if num_entries <= 5:
        height, marker_size, line_length = 400, 10, 0.15
    elif num_entries <= 10:
        height, marker_size, line_length = 500, 12, 0.2
    else:
        height, marker_size, line_length = 600, 12, 0.2

    offsets = [
        line_length if i % 2 == 0 else -line_length
        for i in range(num_entries)
    ]

    fig = go.Figure()

    # =========================
    # 🔁 Central line
    # =========================
    if layout_mode == "Horizontal":
        fig.add_shape(
            type="line",
            x0=-0.5, x1=num_entries - 0.5,
            y0=0, y1=0,
            line=dict(color="gray", width=2)
        )
    else:
        fig.add_shape(
            type="line",
            x0=0, x1=0,
            y0=-0.5, y1=num_entries - 0.5,
            line=dict(color="gray", width=2)
        )

    # =========================
    # 🕰️ Timeline entries
    # =========================
    for i, off in enumerate(offsets):
        date = grouped["Date"][i]
        events = grouped["Event"][i]
        text_height = estimate_text_height(events)

        if layout_mode == "Horizontal":
            x0, y0 = i, 0
            x1, y1 = i, off
            xshift, yshift = 0, text_height if off > 0 else -text_height
        else:
            x0, y0 = 0, i
            x1, y1 = off, i
            xshift, yshift = text_height if off > 0 else -text_height, 0

        # connector
        fig.add_shape(
            type="line",
            x0=x0, y0=y0,
            x1=x1, y1=y1,
            line=dict(color="gray", width=1)
        )

        # bullet
        fig.add_trace(go.Scatter(
            x=[x1], y=[y1],
            mode="markers",
            marker=dict(size=marker_size, color="royalblue"),
            hoverinfo="text",
            hovertext=f"<b>{date}</b><br>" + "<br>".join(events),
            showlegend=False
        ))

        # annotation
        fig.add_annotation(
            x=x1,
            y=y1,
            text=f"<b>{date}</b><br>{format_events(events)}",
            showarrow=False,
            xshift=xshift,
            yshift=yshift,
            align="left",
            font=dict(size=11)
        )

    fig.update_layout(
        height=height if layout_mode == "Horizontal" else height + 300,
        title="Timeline",
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=80, b=40),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "💾 Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "timeline.csv",
        "text/csv"
    )


def gant_timeline():
    st.set_page_config(page_title="Timeline Gant", layout="wide")

    df = pd.read_csv("data/csvs/Gant.csv")

    df["Start date"] = pd.to_datetime(
    df["Start date"],
    format="%d/%m/%y",
    errors="coerce"
    )   

    df["End date"] = pd.to_datetime(
        df["End date"],
        format="%d/%m/%y",
        errors="coerce"
    )

    tasks = df["Event"]
    start = df["Start date"]
    end = df["End date"]
    

    fig = px.timeline(
        df,
        x_start=start,
        x_end=end,
        y=tasks,
        color=tasks,
        title="Gant chart",
        hover_data={
                "Start date": True,
                "End date": True,
                "Παρατηρήσεις": True
                 }  
                )

    st.plotly_chart(fig,use_container_width=True)





def gant_timeline_app(folder="data/csvs"):
    st.set_page_config(page_title="Gantt Timeline", layout="wide")

    # =========================
    # 📂 Load or edit data
    # =========================
    df = dataframe_explorer3(folder, key_prefix="gantt")
    if df is None or df.empty:
        st.stop()

    # =========================
    # ⚙️ Validation
    # =========================
    required_cols = {"Event", "Start date", "End date"}
    if not required_cols.issubset(df.columns):
        st.warning(f"❗ Απαιτούνται οι στήλες: {required_cols}")
        st.stop()

    # =========================
    # 📅 Date parsing
    # =========================
    df["Start date"] = pd.to_datetime(df["Start date"], dayfirst=True, errors="coerce")
    df["End date"] = pd.to_datetime(df["End date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Start date", "End date"])

    # =========================
    # 📊 Gantt chart
    # =========================
    fig = px.timeline(
        df,
        x_start="Start date",
        x_end="End date",
        y="Event",
        color="Event",
        title="Gantt Chart",
        hover_name="Event",
        hover_data={
            "Start date": True,
            "End date": True,
            "Παρατηρήσεις": True
        }
    )

    fig.update_yaxes(autorange="reversed")  # κλασικό Gantt look
    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 💾 Export CSV
    # =========================
    st.download_button(
        "💾 Κατέβασε CSV",
        df.to_csv(index=False).encode("utf-8"),
        "gantt.csv",
        "text/csv"
    )


