
import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("Demo Pydeck: Επιθέσεις & Ταξίδια")

# --- 1️⃣ Δεδομένα επιθέσεων ---
attacks = pd.DataFrame({
    'from_lat': [37.9838, 40.6401],
    'from_lon': [23.7275, 22.9444],
    'to_lat': [38.2466, 35.3387],
    'to_lon': [21.7346, 25.1447],
    'attacker': ['Athens', 'Thessaloniki'],
    'target': ['Patras', 'Heraklion'],
    'strength': [5000, 3000]  # μέγεθος τόξου
})

# ArcLayer για επιθέσεις
attack_layer = pdk.Layer(
    "ArcLayer",
    data=attacks,
    get_source_position='[from_lon, from_lat]',
    get_target_position='[to_lon, to_lat]',
    get_source_color='[255, 0, 0]',
    get_target_color='[0, 0, 255]',
    get_width='strength/1000',
    pickable=True,
    auto_highlight=True
)

# --- 2️⃣ Δεδομένα ταξιδιών ---
journeys = pd.DataFrame({
    'lat': [37.9838, 38.2466, 35.3387],
    'lon': [23.7275, 21.7346, 25.1442],
    'date': ['2026-01-01', '2026-01-10', '2026-01-20']
})

# PathLayer για ταξίδι
journey_layer = pdk.Layer(
    "PathLayer",
    data=[{'path': journeys[['lon','lat']].values.tolist()}],
    get_path='path',
    get_color=[0, 128, 0],
    width_scale=20,
    width_min_pixels=3,
    pickable=True
)

# Scatterplot για σημεία στάσης
journey_points = pdk.Layer(
    "ScatterplotLayer",
    data=journeys,
    get_position='[lon, lat]',
    get_color='[0, 128, 0]',
    get_radius=5000,
    pickable=True
)

# --- 3️⃣ ViewState ---
view_state = pdk.ViewState(
    latitude=38,
    longitude=23.5,
    zoom=5,
    pitch=30
)

# --- 4️⃣ Deck ---
deck = pdk.Deck(
    layers=[attack_layer, journey_layer, journey_points],
    initial_view_state=view_state,
    tooltip={"text": "Αρχή/Τέλος: {attacker} → {target}"}
)

# --- 5️⃣ Προβολή στο Streamlit ---
st.pydeck_chart(deck)


import streamlit as st
import pydeck as pdk
import json

st.title("Κάλυψη χώρας με Pydeck")

# Παράδειγμα: φορτώνουμε GeoJSON για Ελλάδα (μπορεί να το κατεβάσεις από Natural Earth ή άλλο open-source)
with open("greece.geojson") as f:
    greece_geojson = json.load(f)

# GeoJsonLayer
layer = pdk.Layer(
    "GeoJsonLayer",
    greece_geojson,
    stroked=True,        # εμφάνιση περιγράμματος
    filled=True,         # γεμισμένο εσωτερικό
    get_fill_color=[0, 128, 255, 100],  # RGBA
    get_line_color=[0, 0, 0],
    pickable=True
)

view_state = pdk.ViewState(
    latitude=39,
    longitude=22,
    zoom=5
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{NAME}"}
)

st.pydeck_chart(deck)



