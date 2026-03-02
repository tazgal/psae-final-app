# ********************* ΒΙΒΛΙΟΘΗΚΕΣ *********************
import spacy
from spacy.tokens import Span
import sqlite3
from mod_05_sql import sq_inspect_db, sq_add_table_or_columns, sq_search_and_return_texts,sq_search_to_titles
import folium
import webbrowser
from pathlib import Path
import pydeck as pdk
import folium
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import streamlit as st
import json


# ********************* ΒΟΗΘΗΤΙΚΑ *********************

# https://simplemaps.com/data/world-cities
# https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en&sort=name
# geo_new.db
geo_dict_Europe = {
    "Athens": (37.9838, 23.7275),
    "Rome": (41.9028, 12.4964),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Madrid": (40.4168, -3.7038),
    "Lisbon": (38.7169, -9.1390),
    "Vienna": (48.2082, 16.3738),
    "Brussels": (50.8503, 4.3517),
    "Amsterdam": (52.3676, 4.9041),
    "Warsaw": (52.2297, 21.0122),
    "Prague": (50.0755, 14.4378),
    "Budapest": (47.4979, 19.0402),
    "Sofia": (42.6977, 23.3219),
    "Copenhagen": (55.6761, 12.5683),
    "Oslo": (59.9139, 10.7522),
    "Stockholm": (59.3293, 18.0686),
    "Helsinki": (60.1699, 24.9384),
    "Tallinn": (59.4370, 24.7536),
    "Riga": (56.9496, 24.1052),
    "Vilnius": (54.6872, 25.2797),
    "Dublin": (53.3331, -6.2489),
    "Reykjavik": (64.1355, -21.8954),
    "Belgrade": (44.8176, 20.4569),
    "Sarajevo": (43.8486, 18.3564),
    "Zagreb": (45.8144, 15.9780),
    "Skopje": (41.9981, 21.4254),
    "Podgorica": (42.4410, 19.2627),
    "Tirana": (41.3275, 19.8189),
    "Ljubljana": (46.0511, 14.5051),
    "Bratislava": (48.1486, 17.1077),
    "Minsk": (53.9006, 27.5590),
    "Moscow": (55.7558, 37.6173),
    "Kiev": (50.4501, 30.5234),  # Κίεβο
    "Chisinau": (47.0105, 28.8638),
    "Bern": (46.9481, 7.4474),
    "London": (51.5074, -0.1278),
    "Luxembourg": (49.6117, 6.1319),
    "Monaco": (43.7384, 7.4246),
    "San Marino": (43.9336, 12.4508),
    "Andorra la Vella": (42.5078, 1.5211),
    "Vaduz": (47.1416, 9.5215),
    "Valletta": (35.8997, 14.5146),
    "Vatican City": (41.9029, 12.4534)
}
geo_dict_Europe_el = {
    "Αθήνα": (37.9838, 23.7275),
    "Ρώμη": (41.9028, 12.4964),
    "Παρίσι": (48.8566, 2.3522),
    "Βερολίνο": (52.5200, 13.4050),
    "Μαδρίτη": (40.4168, -3.7038),
    "Λισαβόνα": (38.7169, -9.1390),
    "Βιέννη": (48.2082, 16.3738),
    "Βρυξέλλες": (50.8503, 4.3517),
    "Άμστερνταμ": (52.3676, 4.9041),
    "Βαρσοβία": (52.2297, 21.0122),
    "Πράγα": (50.0755, 14.4378),
    "Βουδαπέστη": (47.4979, 19.0402),
    "Σόφια": (42.6977, 23.3219),
    "Κοπεγχάγη": (55.6761, 12.5683),
    "Όσλο": (59.9139, 10.7522),
    "Στοκχόλμη": (59.3293, 18.0686),
    "Ελσίνκι": (60.1699, 24.9384),
    "Ταλίν": (59.4370, 24.7536),
    "Ρίγα": (56.9496, 24.1052),
    "Βίλνιους": (54.6872, 25.2797),
    "Δουβλίνο": (53.3331, -6.2489),
    "Ρέικιαβικ": (64.1355, -21.8954),
    "Βελιγράδι": (44.8176, 20.4569),
    "Σαράγεβο": (43.8486, 18.3564),
    "Ζάγκρεμπ": (45.8144, 15.9780),
    "Σκόπια": (41.9981, 21.4254),
    "Ποντγκόριτσα": (42.4410, 19.2627),
    "Τίρανα": (41.3275, 19.8189),
    "Λιουμπλιάνα": (46.0511, 14.5051),
    "Μπρατισλάβα": (48.1486, 17.1077),
    "Μινσκ": (53.9006, 27.5590),
    "Μόσχα": (55.7558, 37.6173),
    "Κίεβο": (50.4501, 30.5234),
    "Κισινάου": (47.0105, 28.8638),
    "Βέρνη": (46.9481, 7.4474),
    "Λονδίνο": (51.5074, -0.1278),
    "Λουξεμβούργο": (49.6117, 6.1319),
    "Μονακό": (43.7384, 7.4246),
    "Άγιος Μαρίνος": (43.9336, 12.4508),
    "Ανδόρρα λα Βέγια": (42.5078, 1.5211),
    "Βαντούζ": (47.1416, 9.5215),
    "Βαλέτα": (35.8997, 14.5146),
    "Πόλη του Βατικανού": (41.9029, 12.4534)
}
def sq_import_multiple_rows_geo(): 
    conn = sqlite3.connect("geo_new.db")
    cursor = conn.cursor()

    # Δημιουργία πίνακα
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        name TEXT PRIMARY KEY,
        latitude REAL,
        longitude REAL
    )
    """)

    data = [
    ("Αθήνα", 37.9838, 23.7275),
    ("Ρώμη", 41.9028, 12.4964),
    ("Παρίσι", 48.8566, 2.3522),
    ("Βερολίνο", 52.5200, 13.4050),
    ("Μαδρίτη", 40.4168, -3.7038),
    ("Λισαβόνα", 38.7169, -9.1390),
    ("Βιέννη", 48.2082, 16.3738),
    ("Βρυξέλλες", 50.8503, 4.3517),
    ("Άμστερνταμ", 52.3676, 4.9041),
    ("Βαρσοβία", 52.2297, 21.0122),
    ("Πράγα", 50.0755, 14.4378),
    ("Βουδαπέστη", 47.4979, 19.0402),
    ("Σόφια", 42.6977, 23.3219),
    ("Κοπεγχάγη", 55.6761, 12.5683),
    ("Όσλο", 59.9139, 10.7522),
    ("Στοκχόλμη", 59.3293, 18.0686),
    ("Ελσίνκι", 60.1699, 24.9384),
    ("Ταλίν", 59.4370, 24.7536),
    ("Ρίγα", 56.9496, 24.1052),
    ("Βίλνιους", 54.6872, 25.2797),
    ("Δουβλίνο", 53.3331, -6.2489),
    ("Ρέικιαβικ", 64.1355, -21.8954),
    ("Βελιγράδι", 44.8176, 20.4569),
    ("Σαράγεβο", 43.8486, 18.3564),
    ("Ζάγκρεμπ", 45.8144, 15.9780),
    ("Σκόπια", 41.9981, 21.4254),
    ("Ποντγκόριτσα", 42.4410, 19.2627),
    ("Τίρανα", 41.3275, 19.8189),
    ("Λιουμπλιάνα", 46.0511, 14.5051),
    ("Μπρατισλάβα", 48.1486, 17.1077),
    ("Μινσκ", 53.9006, 27.5590),
    ("Μόσχα", 55.7558, 37.6173),
    ("Κίεβο", 50.4501, 30.5234),
    ("Κισινάου", 47.0105, 28.8638),
    ("Βέρνη", 46.9481, 7.4474),
    ("Λονδίνο", 51.5074, -0.1278),
    ("Λουξεμβούργο", 49.6117, 6.1319),
    ("Μονακό", 43.7384, 7.4246),
    ("Άγιος Μαρίνος", 43.9336, 12.4508),
    ("Ανδόρρα λα Βέγια", 42.5078, 1.5211),
    ("Βαντούζ", 47.1416, 9.5215),
    ("Βαλέτα", 35.8997, 14.5146),
    ("Πόλη του Βατικανού", 41.9029, 12.4534)
    ]

  
    cursor.executemany("INSERT OR IGNORE INTO locations VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()
    print("data added")
european_capitals = [
    (37.9838, 23.7275, "Αθήνα"),
    (41.9028, 12.4964, "Ρώμη"),
    (48.8566, 2.3522, "Παρίσι"),
    (52.5200, 13.4050, "Βερολίνο"),
    (40.4168, -3.7038, "Μαδρίτη"),
    (38.7169, -9.1390, "Λισαβόνα"),
    (48.2082, 16.3738, "Βιέννη"),
    (50.8503, 4.3517, "Βρυξέλλες"),
    (52.3676, 4.9041, "Άμστερνταμ"),
    (52.2297, 21.0122, "Βαρσοβία"),
    (50.0755, 14.4378, "Πράγα"),
    (47.4979, 19.0402, "Βουδαπέστη"),
    (42.6977, 23.3219, "Σόφια"),
    (55.6761, 12.5683, "Κοπεγχάγη"),
    (59.9139, 10.7522, "Όσλο"),
    (59.3293, 18.0686, "Στοκχόλμη"),
    (60.1699, 24.9384, "Ελσίνκι"),
    (59.4370, 24.7536, "Ταλίν"),
    (56.9496, 24.1052, "Ρίγα"),
    (54.6872, 25.2797, "Βίλνιους"),
    (53.3331, -6.2489, "Δουβλίνο"),
    (64.1355, -21.8954, "Ρέικιαβικ"),
    (44.8176, 20.4569, "Βελιγράδι"),
    (43.8486, 18.3564, "Σαράγεβο"),
    (45.8144, 15.9780, "Ζάγκρεμπ"),
    (41.9981, 21.4254, "Σκόπια"),
    (42.4410, 19.2627, "Ποντγκόριτσα"),
    (41.3275, 19.8189, "Τίρανα"),
    (46.0511, 14.5051, "Λιουμπλιάνα"),
    (48.1486, 17.1077, "Μπρατισλάβα"),
    (53.9006, 27.5590, "Μινσκ"),
    (55.7558, 37.6173, "Μόσχα"),
    (50.4501, 30.5234, "Κίεβο"),
    (47.0105, 28.8638, "Κισινάου"),
    (46.9481, 7.4474, "Βέρνη"),
    (51.5074, -0.1278, "Λονδίνο"),
    (49.6117, 6.1319, "Λουξεμβούργο"),
    (43.7384, 7.4246, "Μονακό"),
    (43.9336, 12.4508, "Άγιος Μαρίνος"),
    (42.5078, 1.5211, "Ανδόρρα λα Βέγια"),
    (47.1416, 9.5215, "Βαντούζ"),
    (35.8997, 14.5146, "Βαλέτα"),
    (41.9029, 12.4534, "Πόλη του Βατικανού")
]
geo_list_all_el = [

    # 🇪🇺 Ευρώπη
    (37.9838, 23.7275, "Αθήνα"),
    (41.9028, 12.4964, "Ρώμη"),
    (48.8566, 2.3522, "Παρίσι"),
    (52.5200, 13.4050, "Βερολίνο"),
    (40.4168, -3.7038, "Μαδρίτη"),
    (38.7169, -9.1390, "Λισαβόνα"),
    (48.2082, 16.3738, "Βιέννη"),
    (50.8503, 4.3517, "Βρυξέλλες"),
    (52.3676, 4.9041, "Άμστερνταμ"),
    (52.2297, 21.0122, "Βαρσοβία"),
    (50.0755, 14.4378, "Πράγα"),
    (47.4979, 19.0402, "Βουδαπέστη"),
    (42.6977, 23.3219, "Σόφια"),
    (55.6761, 12.5683, "Κοπεγχάγη"),
    (59.3293, 18.0686, "Στοκχόλμη"),
    (60.1699, 24.9384, "Ελσίνκι"),
    (59.4370, 24.7536, "Ταλίν"),
    (56.9496, 24.1052, "Ρίγα"),
    (54.6872, 25.2797, "Βίλνιους"),
    (53.3331, -6.2489, "Δουβλίνο"),
    (64.1355, -21.8954, "Ρέικιαβικ"),
    (44.8176, 20.4569, "Βελιγράδι"),
    (43.8486, 18.3564, "Σαράγεβο"),
    (45.8144, 15.9780, "Ζάγκρεμπ"),
    (41.9981, 21.4254, "Σκόπια"),
    (42.4410, 19.2627, "Ποντγκόριτσα"),
    (41.3275, 19.8189, "Τίρανα"),
    (46.0511, 14.5051, "Λιουμπλιάνα"),
    (48.1486, 17.1077, "Μπρατισλάβα"),
    (53.9006, 27.5590, "Μινσκ"),
    (55.7558, 37.6173, "Μόσχα"),
    (50.4501, 30.5234, "Κίεβο"),
    (47.0105, 28.8638, "Κισινάου"),
    (46.9481, 7.4474, "Βέρνη"),
    (51.5074, -0.1278, "Λονδίνο"),
    (49.6117, 6.1319, "Λουξεμβούργο"),
    (43.7384, 7.4246, "Μονακό"),
    (43.9336, 12.4508, "Άγιος Μαρίνος"),
    (42.5078, 1.5211, "Ανδόρρα λα Βέγια"),
    (47.1416, 9.5215, "Βαντούζ"),
    (35.8997, 14.5146, "Βαλέτα"),
    (41.9029, 12.4534, "Πόλη του Βατικανού"),
    (39.9254, 32.8663, "Άγκυρα"),

    # 🌍 Μέση Ανατολή
    (31.7683, 35.2137, "Ιερουσαλήμ"),

    # 🌎 Βόρεια Αμερική
    (45.4215, -75.6972, "Οττάβα"),
    (38.9072, -77.0369, "Ουάσινγκτον"),
    (19.4326, -99.1332, "Πόλη του Μεξικού"),

    # 🌎 Κεντρική Αμερική
    (14.6349, -90.5069, "Γουατεμάλα Σίτι"),
    (17.2510, -88.7590, "Μπελμοπάν"),
    (14.0723, -87.1921, "Τεγουσιγάλπα"),
    (13.6929, -89.2182, "Σαν Σαλβαδόρ"),
    (12.1149, -86.2362, "Μανάγκουα"),
    (9.9281, -84.0907, "Σαν Χοσέ"),
    (8.9824, -79.5199, "Πόλη του Παναμά"),

    # 🌎 Καραϊβική
    (23.1136, -82.3666, "Αβάνα"),
    (18.5944, -72.3074, "Πορτ-ο-Πρενς"),
    (18.4861, -69.9312, "Σάντο Ντομίνγκο"),
    (17.9712, -76.7936, "Κίνγκστον"),
    (25.0443, -77.3504, "Νασάου"),
    (13.0975, -59.6167, "Μπρίτζταουν"),
    (10.6549, -61.5019, "Πορτ οφ Σπέιν"),

    # 🌎 Νότια Αμερική
    (-34.6037, -58.3816, "Μπουένος Άιρες"),
    (-16.4897, -68.1193, "Λα Παζ"),
    (-15.7939, -47.8828, "Μπραζίλια"),
    (-33.4489, -70.6693, "Σαντιάγο"),
    (4.7110, -74.0721, "Μπογκοτά"),
    (-0.1807, -78.4678, "Κίτο"),
    (6.8013, -58.1551, "Τζώρτζταουν"),
    (-25.2637, -57.5759, "Ασουνσιόν"),
    (-12.0464, -77.0428, "Λίμα"),
    (5.8520, -55.2038, "Παραμαρίμπο"),
    (-34.9011, -56.1645, "Μοντεβιδέο"),
    (10.4806, -66.9036, "Καράκας"),

    # ➕ Ασία
    (39.9042, 116.4074, "Πεκίνο"),
    (28.6139, 77.2090, "Νέο Δελχί")
]

geo_list_all_el_mixed = [
    (37.9838, 23.7275, "Αθήνα"),
    (41.9028, 12.4964, "Ρώμη"),
    (48.8566, 2.3522, "Παρίσι"),
    (52.5200, 13.4050, "Βερολίνο"),
    (40.4168, -3.7038, "Μαδρίτη"),
    (38.7169, -9.1390, "Λισαβόνα"),
    (48.2082, 16.3738, "Βιέννη"),
    (50.8503, 4.3517, "Βρυξέλλες"),
    (52.3676, 4.9041, "Άμστερνταμ"),
    (52.2297, 21.0122, "Βαρσοβία"),
    (50.0755, 14.4378, "Πράγα"),
    (47.4979, 19.0402, "Βουδαπέστη"),
    (42.6977, 23.3219, "Σόφια"),
    (55.6761, 12.5683, "Κοπεγχάγη"),
    (59.9139, 10.7522, "Όσλο"),
    (59.3293, 18.0686, "Στοκχόλμη"),
    (60.1699, 24.9384, "Ελσίνκι"),
    (59.4370, 24.7536, "Ταλίν"),
    (56.9496, 24.1052, "Ρίγα"),
    (54.6872, 25.2797, "Βίλνιους"),
    (53.3331, -6.2489, "Δουβλίνο"),
    (64.1355, -21.8954, "Ρέικιαβικ"),
    (44.8176, 20.4569, "Βελιγράδι"),
    (43.8486, 18.3564, "Σαράγεβο"),
    (45.8144, 15.9780, "Ζάγκρεμπ"),
    (41.9981, 21.4254, "Σκόπια"),
    (42.4410, 19.2627, "Ποντγκόριτσα"),
    (41.3275, 19.8189, "Τίρανα"),
    (46.0511, 14.5051, "Λιουμπλιάνα"),
    (48.1486, 17.1077, "Μπρατισλάβα"),
    (53.9006, 27.5590, "Μινσκ"),
    (55.7558, 37.6173, "Μόσχα"),
    (50.4501, 30.5234, "Κίεβο"),
    (47.0105, 28.8638, "Κισινάου"),
    (46.9481, 7.4474, "Βέρνη"),
    (51.5074, -0.1278, "Λονδίνο"),
    (49.6117, 6.1319, "Λουξεμβούργο"),
    (43.7384, 7.4246, "Μονακό"),
    (43.9336, 12.4508, "Άγιος Μαρίνος"),
    (42.5078, 1.5211, "Ανδόρρα λα Βέγια"),
    (47.1416, 9.5215, "Βαντούζ"),
    (35.8997, 14.5146, "Βαλέτα"),
    (41.9029, 12.4534, "Πόλη του Βατικανού"),
    (48.3794, 31.1656, "Ουκρανία"),
    (37.0902, -95.7129, "ΗΠΑ"),
    (47.4979, 19.0402, "Βουδαπέστη"),
    (38.9637, 35.2433, "Τουρκία"),
    (37.9838, 23.7275, "Αθήνα"),
    (48.8566, 2.3522, "Παρίσι"),
    (20.5937, 78.9629, "Ινδίας"),
    (46.6034, 1.8883, "Γαλλίας"),
    (41.8719, 12.5674, "Ιταλίας"),
    (61.5240, 105.3188, "Ρωσία"),
    (31.3547, 34.3088, "Γάζα"),
    (31.0461, 34.8516, "Ισραήλ"),
    (61.5240, 105.3188, "Ρωσίας"),
    (64.2008, -149.4937, "Αλάσκα"),
    (38.9072, -77.0369, "Ουάσινγκτον"),
    (54.5260, 15.2551, "Ευρώπη"),
    (38.2466, 21.7345, "Πάτρα"),
    (51.9194, 19.1451, "Πολωνία"),
    (35.1264, 33.4299, "Κύπρο"),
    (33.5138, 36.2765, "Συρία"),
    (6.4238, -66.5897, "Βενεζουέλα"),
    (60.4720, 8.4689, "Νορβηγίας"),
    (39.9254, 32.8663, "Άγκυρας"),
    (42.8746, 74.5698, "Κιρόγα"),
    (35.8617, 104.1954, "Κίνα"),
    (39.0742, 21.8243, "Ελλάδα"),
    (48.0159, 37.8028, "Ντονμπάς"),
    (38.8253, 20.7069, "Λευκάδα"),
    (41.8719, 12.5674, "Ιταλία"),
    (51.1657, 10.4515, "Γερμανία"),
    (35.9078, 127.7669, "Νότια Κορέα"),
    (20.5937, 78.9629, "Ινδία"),
    (40.0691, 45.0382, "Αρμενίων"),
    (40.9142, 38.3893, "Πόντου"),
    (55.3781, -3.4360, "Βρετανία"),
    (37.5665, 126.9780, "Σεούλ"),
    (50.5039, 4.4699, "Βέλγιο"),
    (47.0105, 28.8638, "Κισινάου"),
    (50.4501, 30.5234, "Κίεβο"),
    (42.7087, 19.3744, "Μαυροβούνιο"),
    (39.9042, 116.4074, "Πεκίνο"),
    (71.7069, -42.6043, "Γροιλανδία"),
    (23.6345, -102.5528, "Μεξικό"),
    (64.9631, -19.0208, "Ισλανδία"),
    (47.1625, 19.5033, "Ουγγαρία"),
    (35.9375, 14.3754, "Μάλτας"),
    (50.1109, 8.6821, "ΕΕ")
]



geo_dict_all_new_el = {name: (lat, lon) for lat, lon, name in geo_list_all_el}

# Folium: ιδανικό για γρήγορους, διαδραστικούς χάρτες σε HTML.
# GeoPandas: χειρισμός χωρικών δεδομένων, φιλτράρισμα, συγχωνεύσεις.
# Plotly: για διαδραστικά γραφήματα και scattermaps, μπορεί να συνδυαστεί με GeoJSON.


# ********************* DEFS *********************

# Spacy - Παίρνει κείμενο και με το εξωτερικό λεξικό συντεταγμένων προσθέτει labels με συντεταγμένες σε πόλεις (και εμφανίζει)
def geo_spacy_coordinates(newtext, cdict):
    Span.set_extension("coordinates", default = None, force = True)
    nlp = spacy.load("el_core_news_sm")
    @spacy.language.Language.component("geotag")

    def geotag(doc):
        for ent in doc.ents:
            if ent.label_ == "GPE" and ent.text in cdict:
                ent._.coordinates = cdict[ent.text]
        return doc

    nlp.add_pipe("geotag",after="ner")

    doc = nlp(newtext)

    list_coord =[]

    for ent in doc.ents:
        if ent.label_ == "GPE" and ent._.coordinates is not None:
            p = (ent.text, ent._.coordinates)
            print(p)
            list_coord.append(p)

    return list_coord    

# Το ίδιο αλλά τραβάει από εξωτερική ΒΔ τα ονόματα
def spacy_coordinates_from_db(text):
    # Ορίζω extension "coords"
    Span.set_extension("coords", default=None, force=True)

    # Σύνδεση με SQLite
    conn = sqlite3.connect("geo_new.db")
    cursor = conn.cursor()

    nlp = spacy.load("el_core_news_sm")

    @spacy.language.Language.component("geo_component")
    def geo_component(doc):
        for ent in doc.ents:
            if ent.label_ == "GPE":  # GPE = Geo-Political Entity
                cursor.execute("SELECT latitude, longitude FROM locations WHERE name=?", (ent.text,))
                row = cursor.fetchone()
                if row:
                    ent._.coords = row  # Αποθηκεύω (lat, long)
        return doc

    nlp.add_pipe("geo_component", after="ner")

    doc = nlp(text)

    for ent in doc.ents:
        print(ent.text, ent.label_, ent._.coords)

# FOLIUM - Παίρνει ένα σημείο και το προβάλλει στον χάρτη 
def fol_pin():
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=6)

    folium.Marker(location=[37.9838, 23.7275], popup="Athens").add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m

# Εμφανίζει και ένα κείμενο που του δίνεις όταν περνάει ο κέρσορας πάνω από την πινέζα 
def fol_pin_with_text(text):
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=6)

    folium.Marker(location=[37.9838, 23.7275], popup="Athens", tooltip=text).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m

# Παίρνει μια λίστα με lat, lon, ονόματα κτλ και την προβάλλει στον χάρτη
def fol_pin_list(list):
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    for name, (lat, lon) in list:
        folium.Marker(location=[lat, lon], popup=name).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m

def fol_pin_list_with_text(list,text):
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    for name, (lat, lon) in list:
        folium.Marker(location=[lat, lon], popup=name,tooltip=text).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m


# Παίρνει ένα λεξικό και το προβάλλει στο χάρτη 
def fol_pin_dict(dict):
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    for name, (lat, lon) in dict.items():  # Χρησιμοποιούμε items() αντί για απλό for
        folium.Marker(location=[lat, lon], popup=name).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m

# Το ίδιο αλλά προβάλλει και ένα κείμενο ... αλλά πάνω σε όλες τις πινέζες
def fol_pin_dict_with_text(dict,text):
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    for name, (lat, lon) in dict.items():  # Χρησιμοποιούμε items() αντί για απλό for
        folium.Marker(location=[lat, lon], popup=name,tooltip=text).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m

def fol_pin_dict_with_text2(dict, text):
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    for name, (lat, lon) in dict.items():
        # HTML popup με scroll αν το κείμενο είναι μεγάλο
        popup_html = f"""
        <div style="width:250px; height:150px; overflow:auto;">
            <h4>{name}</h4>
            <p>{text}</p>
        </div>
        """
        popup = folium.Popup(popup_html, max_width=300)

        folium.Marker(
            location=[lat, lon],
            tooltip=name,   # εμφανίζεται όταν περνάς το ποντίκι
            popup=popup     # εμφανίζεται όταν κάνεις κλικ
        ).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)

    # Μετατροπή σε πλήρες URL για webbrowser
    webbrowser.open(map_path.resolve().as_uri())

    return m

# 1. Κάνει search με λέξη κλειδί στο κείμενο των ειδήσεων στη ΒΔ
# 2. "Τραβάει" από εξωτερικό λεξικό συντεταγμένες και τις κολλάει σε ανάλογες οντότητες που η Spacy αναγνωρίζει ως GPE 
# 3. Προβάλει με folium τις σχετικές πινέζες στο χάρτη 
def scr_from_db_to_map():
    newstext = sq_search_and_return_texts()
    x = geo_spacy_coordinates(newstext, geo_dict_all_new_el)
    fol_pin_list(x)

def scr_from_text_to_map_streamlit(text):
    x = geo_spacy_coordinates(text, geo_dict_all_new_el)
    fol_pin_list(x)

# ΠΡΟΣΟΧΗ ΛΑΘΟΣ ΒΑΖΕΙ ΤΟ ΙΔΙΟ ΚΕΙΜΕΝΟ 
# 1. Κάνει search με λέξη κλειδί στο κείμενο των ειδήσεων στη ΒΔ
# 2. "Τραβάει" από εξωτερικό λεξικό συντεταγμένες και τις κολλάει σε ανάλογες οντότητες που η Spacy αναγνωρίζει ως GPE 
# 3. Προβάλει με folium τις σχετικές πινέζες στο χάρτη, εμφανίζοντας και το σχετικό κείμενο
def scr_from_db_to_map_with_text():
    newstext = sq_search_and_return_texts()
    x = geo_spacy_coordinates(newstext, geo_dict_all_new_el)
    fol_pin_list_with_text(x,newstext)


# σωστό αλλά δεν δουλεύει (ή μήπως αργεί πολύ;)
def scr_from_db_to_map_with_text2():
    # Παίρνεις όλα τα κείμενα από τη ΒΔ
    texts = sq_search_and_return_texts()
    
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    # Για κάθε κείμενο
    for newstext in texts:
        # Βρίσκεις γεω-οντότητες με συντεταγμένες
        x = geo_spacy_coordinates(newstext, geo_dict_all_new_el)
        
        # Και τις προβάλλεις με το αντίστοιχο κείμενο
        for name, coords in x:
            if coords:  # αν υπάρχουν συντεταγμένες στο λεξικό
                lat, lon = coords
                folium.Marker(
                    location=[lat, lon],
                    popup=name,
                    tooltip=newstext[:300] + "..."  # μικρό απόσπασμα για αναγνωσιμότητα
                ).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)
    webbrowser.open(map_path.resolve().as_uri())

def scr_from_db_to_map_with_text3(texts):
    
    m = folium.Map(location=[37.9838, 23.7275], zoom_start=3)

    # Για κάθε κείμενο
    for newstext in texts:
        # Βρίσκεις γεω-οντότητες με συντεταγμένες
        x = geo_spacy_coordinates(newstext, geo_dict_all_new_el)
        
        # Και τις προβάλλεις με το αντίστοιχο κείμενο
        for name, coords in x:
            if coords:  # αν υπάρχουν συντεταγμένες στο λεξικό
                lat, lon = coords
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(newstext, max_width=250),
                    tooltip=name
                ).add_to(m)

    map_path = Path("/Users/tazgal/DIGITAL_HUMANITITES/ΨΑΕ_πτυχιακή_όλα/test_map.html")
    m.save(map_path)
    webbrowser.open(map_path.resolve().as_uri())

# ********************* TEST AREA *********************

def fol_pin_list2(pin_list):
    m = folium.Map(
        location=[37.9838, 23.7275],
        zoom_start=4,
        tiles="OpenStreetMap"
    )

    for name, (lat, lon) in pin_list:
        folium.Marker(
            location=[lat, lon],
            popup=name,
            tooltip=name
        ).add_to(m)

    st_folium(m, width=1000, height=800)


def scr_from_text_to_map_streamlit2(text):
    x = geo_spacy_coordinates(text, geo_dict_all_new_el)
    fol_pin_list2(x)


COUNTRY_MAP1 = {
    "Ελλάδα": "GR",
    "Γαλλία": "FR",
    "Ιταλία": "IT",
    "Γερμανία": "DE",
    "Ισπανία": "ES",
    "Τουρκία": "TR",
    "Ρωσία": "RU",
    "ΗΠΑ": "US",
    "Κίνα": "CN",
    "Ινδία": "IN",
    "Ουκρανία": "UA",
    "Ισραήλ": "IL",
    "Βρετανία": "GB"
}

COUNTRY_MAP = {
    "Ελλάδα": "Greece",
    "Γαλλία": "France",
    "Ιταλία": "Italy",
    "Γερμανία": "Germany",
    "Ισπανία": "Spain",
    "Τουρκία": "Turkey",
    "Ρωσία": "Russia",
    "ΗΠΑ": "United States",
    "Κίνα": "China",
    "Ινδία": "India",
    "Ουκρανία": "Ukraine",
    "Ισραήλ": "Israel",
    "Βρετανία": "United Kingdom",
    # Προσθέτουμε και αγγλικά για να τα αναγνωρίζει απευθείας
    "Greece": "Greece",
    "France": "France",
    "Italy": "Italy",
    "Germany": "Germany",
    "Spain": "Spain",
    "Turkey": "Turkey",
    "Russia": "Russia",
    "United States": "United States",
    "China": "China",
    "India": "India",
    "Ukraine": "Ukraine",
    "Israel": "Israel",
    "United Kingdom": "United Kingdom",
}


country_translations = {
    "Afghanistan": "Αφγανιστάν",
    "Angola": "Αγκόλα",
    "Albania": "Αλβανία",
    "United Arab Emirates": "Ηνωμένα Αραβικά Εμιράτα",
    "Argentina": "Αργεντινή",
    "Armenia": "Αρμενία",
    "Antarctica": "Ανταρκτική",
    "Australia": "Αυστραλία",
    "Austria": "Αυστρία",
    "Azerbaijan": "Αζερμπαϊτζάν",
    "Burundi": "Μπουρούντι",
    "Belgium": "Βέλγιο",
    "Benin": "Μπενίν",
    "Burkina Faso": "Μπουρκίνα Φάσο",
    "Bangladesh": "Μπανγκλαντές",
    "Bulgaria": "Βουλγαρία",
    "The Bahamas": "Μπαχάμες",
    "Bosnia and Herzegovina": "Βοσνία και Ερζεγοβίνη",
    "Belarus": "Λευκορωσία",
    "Belize": "Μπελίζ",
    "Bermuda": "Βερμούδες",
    "Bolivia": "Βολιβία",
    "Brazil": "Βραζιλία",
    "Brunei": "Μπρουνέι",
    "Bhutan": "Μπουτάν",
    "Botswana": "Μποτσουάνα",
    "Central African Republic": "Κεντροαφρικανική Δημοκρατία",
    "Canada": "Καναδάς",
    "Switzerland": "Ελβετία",
    "Chile": "Χιλή",
    "China": "Κίνα",
    "Ivory Coast": "Ακτή Ελεφαντοστού",
    "Cameroon": "Καμερούν",
    "Democratic Republic of the Congo": "Λαϊκή Δημοκρατία του Κονγκό",
    "Republic of the Congo": "Δημοκρατία του Κονγκό",
    "Colombia": "Κολομβία",
    "Costa Rica": "Κόστα Ρίκα",
    "Cuba": "Κούβα",
    "Northern Cyprus": "Βόρεια Κύπρος",
    "Cyprus": "Κύπρος",
    "Czech Republic": "Τσεχία",
    "Germany": "Γερμανία",
    "Djibouti": "Τζιμπουτί",
    "Denmark": "Δανία",
    "Dominican Republic": "Δομινικανή Δημοκρατία",
    "Algeria": "Αλγερία",
    "Ecuador": "Ισημερινός",
    "Egypt": "Αίγυπτος",
    "Eritrea": "Ερυθραία",
    "Spain": "Ισπανία",
    "Estonia": "Εσθονία",
    "Ethiopia": "Αιθιοπία",
    "Finland": "Φινλανδία",
    "Fiji": "Φίτζι",
    "Falkland Islands": "Νήσοι Φόκλαντ",
    "France": "Γαλλία",
    "Gabon": "Γκαμπόν",
    "United Kingdom": "Ηνωμένο Βασίλειο",
    "Georgia": "Γεωργία",
    "Ghana": "Γκάνα",
    "Guinea": "Γουινέα",
    "Gambia": "Γκάμπια",
    "Guinea Bissau": "Γουινέα Μπισσάου",
    "Equatorial Guinea": "Ισημερινή Γουινέα",
    "Greece": "Ελλάδα",
    "Greenland": "Γροιλανδία",
    "Guatemala": "Γουατεμάλα",
    "French Guiana": "Γαλλική Γουιάνα",
    "Guyana": "Γουιάνα",
    "Honduras": "Ονδούρα",
    "Croatia": "Κροατία",
    "Haiti": "Αϊτή",
    "Hungary": "Ουγγαρία",
    "Indonesia": "Ινδονησία",
    "Ireland": "Ιρλανδία",
    "Iran": "Ιράν",
    "Iraq": "Ιράκ",
    "Iceland": "Ισλανδία",
    "Israel": "Ισραήλ",
    "Italy": "Ιταλία",
}

def choropleth_from_text():
    st.subheader("Χάρτης χωρών από κείμενο")

    text = st.text_area("Εισάγετε κείμενο:", height=200)

    if not st.button("Δημιουργία χάρτη"):
        return

    if not text.strip():
        st.info("Γράψτε ή επικολλήστε κείμενο.")
        return

    # Αναζήτηση χωρών στο κείμενο
    found = []
    for country_input, country_en in COUNTRY_MAP.items():
        count = text.count(country_input)
        if count > 0:
            found.append((country_en, count))

    if not found:
        st.warning("Δεν εντοπίστηκαν χώρες.")
        return

    # DataFrame για Folium
    df = pd.DataFrame(found, columns=["country", "count"])

    # Φόρτωση GeoJSON
    with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
        geo = json.load(f)

    # Δημιουργία Folium χάρτη
    m = folium.Map(location=[50, 10], zoom_start=3)

    folium.Choropleth(
        geo_data=geo,
        data=df,
        columns=["country", "count"],
        key_on="properties.name",  # ταιριάζει με GeoJSON
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Αναφορές χωρών"
    ).add_to(m)

    st_folium(m, width=800, height=550)

def choropleth_from_text2():
    st.subheader("Χάρτης χωρών από κείμενο")

    text = st.text_area("Εισάγετε κείμενο:", height=200)
    
    # Button για δημιουργία χάρτη
    if st.button("Δημιουργία χάρτη"):
        if not text.strip():
            st.info("Γράψτε ή επικολλήστε κείμενο.")
            return

        # Εδώ δημιουργούμε το df και το map
        df = pd.DataFrame({"country": ["Greece"], "count": [5]})
        
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            geo = json.load(f)

        m = folium.Map(location=[50, 10], zoom_start=3)

        folium.Choropleth(
            geo_data=geo,
            data=df,
            columns=["country", "count"],
            key_on="properties.name",
            fill_color="YlOrRd",
        ).add_to(m)

        # Εμφάνιση χάρτη
        st_folium(m, width=800, height=550)



def choropleth_from_text3():
    st.subheader("Χάρτης χωρών από κείμενο")

    # Φόρτωση GeoJSON μόνο μία φορά
    if "geojson" not in st.session_state:
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    # Text area
    text = st.text_area("Εισάγετε κείμενο:", height=200)

    # Button για δημιουργία χάρτη
    if st.button("Δημιουργία χάρτη"):
        if not text.strip():
            st.info("Γράψτε ή επικολλήστε κείμενο.")
        else:
            # Παράδειγμα: count για Ελλάδα
            df = pd.DataFrame({"country": ["Greece"], "count": [1]})

            # Δημιουργία Folium map
            m = folium.Map(location=[50, 10], zoom_start=3)

            folium.Choropleth(
                geo_data=st.session_state.geojson,
                data=df,
                columns=["country", "count"],
                key_on="properties.name",
                fill_color="YlOrRd",
                fill_opacity=0.7,
                line_opacity=0.3,
                legend_name="Αναφορές χωρών"
            ).add_to(m)

            # Αποθήκευση map στο session_state
            st.session_state.map = m

    # Αν υπάρχει ήδη map στο session_state, το εμφανίζουμε
    if "map" in st.session_state:
        st_folium(st.session_state.map, width=800, height=1050)

 
def basic_map():
    st.write("Basic Map")

    m = folium.Map(location=[50,70],zoom_start=3)

    st_folium(m,height=600,width=1200)


def map_with_json():
    st.subheader("Map with geojson")

    if "geojson" not in st.session_state:
        with open ("data/maps/world_countries.geojson",encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    m = folium.Map(location=[50,60],zoom_start=3)

    folium.GeoJson(st.session_state.geojson, name="countries").add_to(m)

    st_folium(m,width=1200,height=600)


def choropleth_example():
    st.subheader("Choropleth με απλά δεδομένα")

    # Φόρτωση GeoJSON μία φορά
    if "geojson" not in st.session_state:
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    # Δημιουργία Folium map
    m = folium.Map(location=[50, 10], zoom_start=3)

    # Δεδομένα για choropleth
    # columns: "country" πρέπει να ταιριάζει με properties.name στο GeoJSON
    data = {
        "country": ["Greece", "Italy", "France", "Germany"],
        "value": [10, 20, 15, 30]
    }
    df = pd.DataFrame(data)

    # Δημιουργία choropleth
    folium.Choropleth(
        geo_data=st.session_state.geojson,
        data=df,
        columns=["country", "value"],
        key_on="properties.name",  # πρέπει να ταιριάζει με GeoJSON
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Παράδειγμα Τιμών"
    ).add_to(m)

    # Εμφάνιση χάρτη
    st_folium(m, width=800, height=550)




# Mapping ελληνικά -> αγγλικά
GREEK_TO_EN = {
    "Ελλάδα": "Greece",
    "Γαλλία": "France",
    "Ιταλία": "Italy",
    "Γερμανία": "Germany",
    "Ισπανία": "Spain",
    "Τουρκία": "Turkey",
    "Ρωσία": "Russia",
    "ΗΠΑ": "United States",
    "Κίνα": "China",
    "Ινδία": "India",
    "Ουκρανία": "Ukraine",
    "Ισραήλ": "Israel",
    "Βρετανία": "United Kingdom"
}


def choropleth_from_text5(text):
    st.subheader("Χάρτης χωρών από κείμενο")

    # Φόρτωση GeoJSON μία φορά
    if "geojson" not in st.session_state:
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    # Button για δημιουργία χάρτη
    if st.button("Δημιουργία χάρτη"):
        if not text.strip():
            st.info("Γράψτε ή επικολλήστε κείμενο.")
            return

        # Μέτρηση εμφανίσεων χωρών στο κείμενο
        found = []
        for gr_name, en_name in GREEK_TO_EN.items():
            count = text.count(gr_name)
            if count > 0:
                found.append((en_name, count))

        # Ελέγχουμε και για αγγλικά ονόματα απευθείας
        for en_name in GREEK_TO_EN.values():
            count = text.count(en_name)
            if count > 0 and (en_name, count) not in found:
                found.append((en_name, count))

        if not found:
            st.warning("Δεν εντοπίστηκαν χώρες.")
            return

        # DataFrame για Folium
        df = pd.DataFrame(found, columns=["country", "count"])

        # Δημιουργία Folium map
        m = folium.Map(location=[50, 10], zoom_start=3)

        folium.Choropleth(
            geo_data=st.session_state.geojson,
            data=df,
            columns=["country", "count"],
            key_on="properties.name",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.3,
            legend_name="Αναφορές χωρών"
        ).add_to(m)

        # Αποθήκευση map στο session_state για να μην εξαφανίζεται
        st.session_state.map = m

    # Εμφάνιση map αν υπάρχει ήδη
    if "map" in st.session_state:
        st_folium(st.session_state.map,width=1000, height=600)


def choropleth_from_text6(text):
    st.subheader("Map from text")

    # Φόρτωση GeoJSON μία φορά
    if "geojson" not in st.session_state:
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    if not text.strip():
        st.info("Write your text")
        return

    # Μέτρηση εμφανίσεων χωρών στο κείμενο
    found = []
    for gr_name, en_name in GREEK_TO_EN.items():
        count = text.count(gr_name)
        if count > 0:
            found.append((en_name, count))

    # Έλεγχος για αγγλικά ονόματα απευθείας
    for en_name in GREEK_TO_EN.values():
        count = text.count(en_name)
        if count > 0 and (en_name, count) not in found:
            found.append((en_name, count))

    if not found:
        st.warning("No countries found")
        return

    # DataFrame για Folium
    df = pd.DataFrame(found, columns=["country", "count"])

    # Δημιουργία Folium map με fit_bounds για να χωράει όλος ο κόσμος
    m = folium.Map()
    m.fit_bounds([[-90, -180], [90, 180]])

    folium.Choropleth(
        geo_data=st.session_state.geojson,
        data=df,
        columns=["country", "count"],
        key_on="properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Αναφορές χωρών"
    ).add_to(m)

    # Αποθήκευση map στο session_state
    st.session_state.map = m

    # Εμφάνιση map
    st_folium(st.session_state.map, width=1000, height=600)


def choropleth_from_text7(text):
    st.subheader("Map from text")

    # Φόρτωση GeoJSON μόνο μία φορά
    if "geojson" not in st.session_state:
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    if not text.strip():
        st.info("Write your text")
        return

    # Μέτρηση χωρών
    found = []

    for gr_name, en_name in GREEK_TO_EN.items():
        count = text.count(gr_name)
        if count > 0:
            found.append((en_name, count))

    for en_name in GREEK_TO_EN.values():
        count = text.count(en_name)
        if count > 0 and (en_name, count) not in found:
            found.append((en_name, count))

    if not found:
        st.warning("No countries found")
        return

    df = pd.DataFrame(found, columns=["country", "count"])

    # Δημιουργία νέου χάρτη κάθε φορά
    m = folium.Map()
    m.fit_bounds([[-90, -180], [90, 180]])

    folium.Choropleth(
        geo_data=st.session_state.geojson,
        data=df,
        columns=["country", "count"],
        key_on="properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Country mentions"
    ).add_to(m)

    # Αποθήκευση
    st.session_state["choropleth_map"] = m

    # Σταθερό key για να μην εξαφανίζεται στο zoom
    st_folium(
        m,
        width=1000,
        height=600,
        key="stable_choropleth"
    )


GREEK_TO_EN = {

    # 🇪🇺 Ευρωπαϊκή Ένωση
    "Αυστρία": "Austria",
    "Βέλγιο": "Belgium",
    "Βουλγαρία": "Bulgaria",
    "Κροατία": "Croatia",
    "Κύπρος": "Cyprus",
    "Τσεχία": "Czechia",
    "Δανία": "Denmark",
    "Εσθονία": "Estonia",
    "Φινλανδία": "Finland",
    "Γαλλία": "France",
    "Γερμανία": "Germany",
    "Ελλάδα": "Greece",
    "Ουγγαρία": "Hungary",
    "Ιρλανδία": "Ireland",
    "Ιταλία": "Italy",
    "Λετονία": "Latvia",
    "Λιθουανία": "Lithuania",
    "Λουξεμβούργο": "Luxembourg",
    "Μάλτα": "Malta",
    "Ολλανδία": "Netherlands",
    "Πολωνία": "Poland",
    "Πορτογαλία": "Portugal",
    "Ρουμανία": "Romania",
    "Σλοβακία": "Slovakia",
    "Σλοβενία": "Slovenia",
    "Ισπανία": "Spain",
    "Σουηδία": "Sweden",
    "Αγγλία": "United Kingdom",
    "Βρετανία": "United Kingdom",

    # 🌎 Βόρεια Αμερική
    "Καναδάς": "Canada",
    "ΗΠΑ": "United States of America",
    "Ηνωμένες Πολιτείες": "United States of America",
    "Μεξικό": "Mexico",

    # 🌎 Κεντρική Αμερική
    "Γουατεμάλα": "Guatemala",
    "Μπελίζ": "Belize",
    "Ονδούρα": "Honduras",
    "Ελ Σαλβαδόρ": "El Salvador",
    "Νικαράγουα": "Nicaragua",
    "Κόστα Ρίκα": "Costa Rica",
    "Παναμάς": "Panama",

    # 🌎 Καραϊβική
    "Κούβα": "Cuba",
    "Αϊτή": "Haiti",
    "Δομινικανή Δημοκρατία": "Dominican Rep.",
    "Τζαμάικα": "Jamaica",
    "Μπαχάμες": "Bahamas",
    "Μπαρμπάντος": "Barbados",
    "Τρινιντάντ και Τομπάγκο": "Trinidad and Tobago",

    # 🌎 Νότια Αμερική
    "Αργεντινή": "Argentina",
    "Βολιβία": "Bolivia",
    "Βραζιλία": "Brazil",
    "Χιλή": "Chile",
    "Κολομβία": "Colombia",
    "Ισημερινός": "Ecuador",
    "Γουιάνα": "Guyana",
    "Παραγουάη": "Paraguay",
    "Περού": "Peru",
    "Σουρινάμ": "Suriname",
    "Ουρουγουάη": "Uruguay",
    "Βενεζουέλα": "Venezuela",

    # ➕ Μεγάλες χώρες
    "Ρωσία": "Russia",
    "Κίνα": "China",
    "Ινδία": "India",

    "Τουρκία": "Turkey",
    "Συρία": "Syria",
    "Λίβανος": "Lebanon",
    "Ισραήλ": "Israel",
    "Παλαιστίνη": "Palestine",
    "Ιορδανία": "Jordan",
    "Ιράκ": "Iraq",
    "Ιράν": "Iran",
    "Σαουδική Αραβία": "Saudi Arabia",
    "Κουβέιτ": "Kuwait",
    "Κατάρ": "Qatar",
    "Μπαχρέιν": "Bahrain",
    "Ηνωμένα Αραβικά Εμιράτα": "United Arab Emirates",
    "Ομάν": "Oman",
    "Υεμένη": "Yemen",
    "Αίγυπτος": "Egypt", 

    "Αφγανιστάν": "Afghanistan",
    "Πακιστάν": "Pakistan",
    "Καζακστάν": "Kazakhstan",
    "Ουζμπεκιστάν": "Uzbekistan",
    "Τουρκμενιστάν": "Turkmenistan",
    "Κιργιστάν": "Kyrgyzstan",
    "Τατζικιστάν": "Tajikistan",

    "Ινδονησία": "Indonesia",
    "Μαλαισία": "Malaysia",
    "Σιγκαπούρη": "Singapore",
    "Ταϊλάνδη": "Thailand",
    "Βιετνάμ": "Vietnam",
    "Λάος": "Laos",
    "Καμπότζη": "Cambodia",
    "Μιανμάρ": "Myanmar",
    "Φιλιππίνες": "Philippines",
    "Μπρουνέι": "Brunei",
    "Ανατολικό Τιμόρ": "Timor-Leste",

    "Νεπάλ": "Nepal",
    "Μπουτάν": "Bhutan",
    "Μπανγκλαντές": "Bangladesh",
    "Σρι Λάνκα": "Sri Lanka",
    "Μαλδίβες": "Maldives",
    "Ινδία": "India"


}


def choropleth_from_text_final(text):
    st.subheader("Χάρτης χωρών από κείμενο")

    # Φόρτωση GeoJSON μία φορά
    if "geojson" not in st.session_state:
        with open("data/maps/world_countries.geojson", encoding="utf-8") as f:
            st.session_state.geojson = json.load(f)

    # Αν το text είναι κενό, βγάζουμε info
    if not text.strip():
        st.info("Γράψτε ή επικολλήστε κείμενο.")
        return

    # Μέτρηση εμφανίσεων χωρών
    found = []
    for gr_name, en_name in GREEK_TO_EN.items():
        count = text.count(gr_name)
        if count > 0:
            found.append((en_name, count))

    # Έλεγχος και για αγγλικά ονόματα απευθείας
    for en_name in GREEK_TO_EN.values():
        count = text.count(en_name)
        if count > 0 and (en_name, count) not in found:
            found.append((en_name, count))

    if not found:
        st.warning("Δεν εντοπίστηκαν χώρες.")
        return

    # DataFrame για Folium
    df = pd.DataFrame(found, columns=["country", "count"])

    # Δημιουργία Folium map με fit_bounds
    m = folium.Map()
    m.fit_bounds([[-90, -180], [90, 180]])

    folium.Choropleth(
        geo_data=st.session_state.geojson,
        data=df,
        columns=["country", "count"],
        key_on="properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Αναφορές χωρών"
    ).add_to(m)

    # Αποθήκευση στο session_state για να μην εξαφανίζεται
    st.session_state.map = m

    # Εμφάνιση map
    st_folium(st.session_state.map, width=1000, height=600, key="world_map")

