import yaml
import streamlit as st
import os
from datetime import datetime
import copy
import json


# folder = "data/economy_files/economy_ymls"

def sync_yaml_to_json(yaml_path):
    json_path = yaml_path.replace(".yaml", ".json")

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def new_yaml4(folder: str):

    st.subheader("Δημιουργία νέου YAML")

    filename = st.text_input("Όνομα αρχείου (χωρίς .yaml)")
    user_text = st.text_area("Βάλτε το κείμενό σας εδώ (σε YAML format)")

    if st.button("Create YAML and JSON"):

        # --- Έλεγχοι ---
        if not filename or not filename.strip():
            st.error("Κενό όνομα αρχείου")
            return None, None

        if not user_text.strip():
            st.error("Δεν έχει δοθεί περιεχόμενο")
            return None, None

        try:
            data_dict = yaml.safe_load(user_text)
        except yaml.YAMLError as e:
            st.error(f"Λάθος YAML format: {e}")
            return None, None

        filename = filename.strip()
        filepath = os.path.join(folder, f"{filename}.yaml")

        if os.path.exists(filepath):
            st.error("Το αρχείο υπάρχει ήδη")
            return None, None

        # --- Template ---
        created = datetime.now().isoformat(timespec="seconds")

        template = {
            "meta": {
                "title": filename,
                "description": "",
                "source": "",
                "created": created,
                "version": 1,
            },
            "data": data_dict
        }

        # --- YAML ---
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                template,
                f,
                allow_unicode=True,
                sort_keys=False
            )

        # --- JSON ---
        json_path = filepath.replace(".yaml", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                template,
                f,
                ensure_ascii=False,
                indent=2
            )

        st.success("YAML και JSON δημιουργήθηκαν επιτυχώς ✅")

        return template, filepath

    return None, None

    


def new_yaml3(folder: str):

    st.subheader("Δημιουργία νέου YAML")

    # 1️⃣ Όνομα αρχείου
    filename = st.text_input("Όνομα αρχείου (χωρίς .yaml)")

    # 2️⃣ Περιεχόμενο του YAML
    user_text = st.text_area("Βάλτε το κείμενό σας εδώ")

    # 3️⃣ Κουμπί υποβολής
    if st.button("Δημιουργία αρχείου YAML"):

        # Validation
        if not filename or not filename.strip():
            st.error("Κενό όνομα αρχείου")
            return None, None

        if not user_text.strip():
            st.error("Δεν έχει δοθεί περιεχόμενο")
            return None, None

        filename = filename.strip()
        filepath = os.path.join(folder, f"{filename}.yaml")

        if os.path.exists(filepath):
            st.error("Το αρχείο υπάρχει ήδη")
            return None, None

        created = datetime.now().isoformat(timespec="seconds")

        # Δημιουργία template YAML
        template = {
            "meta": {
                "title": filename,
                "description": "",
                "created": created,
                "version": 1,
            },
            "data": user_text  # εδώ μπαίνει το περιεχόμενο που γράφτηκε
        }

        # Γράψιμο στο αρχείο
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.safe_dump(template, f, allow_unicode=True, sort_keys=False)

        st.success(f"Το αρχείο δημιουργήθηκε: {filepath}")
        return template, filepath

    return None, None

def new_yaml2(folder: str):

    st.subheader("Δημιουργία νέου YAML")

    filename = st.text_input("Όνομα αρχείου (χωρίς .yaml)")

    create_clicked = st.button("Δημιουργία αρχείου YAML")

    if not create_clicked:
        return None, None

    # ⬇️ validation ΜΟΝΟ αφού πατηθεί το κουμπί
    if not filename or not filename.strip():
        st.error("Κενό όνομα αρχείου")
        return None, None

    filename = filename.strip()
    filepath = os.path.join(folder, f"{filename}.yaml")

    if os.path.exists(filepath):
        st.error("Το αρχείο υπάρχει ήδη")
        return None, None

    created = datetime.now().isoformat(timespec="seconds")

    template = {
        "meta": {
            "title": filename,
            "description": "",
            "created": created,
            "version": 1,
        },
        "data": {},
    }

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.safe_dump(template, f, allow_unicode=True, sort_keys=False)

    st.success(f"Το αρχείο δημιουργήθηκε: {filepath}")

    return template, filepath


def new_yaml(folder: str):

    filename = st.text_input("Όνομα αρχείου (χωρίς .yaml)")

    if not filename:
        return None, None  # ο χρήστης δεν έχει γράψει ακόμη

    if not filename.strip():
        st.error("Κενό όνομα αρχείου")
        return None, None

    filename = filename.strip()
    filepath = os.path.join(folder, f"{filename}.yaml")

    if os.path.exists(filepath):
        st.error("Το αρχείο υπάρχει ήδη")
        return None, None

    created = datetime.now().isoformat(timespec="seconds")

    template = {
        "meta": {
            "title": filename,
            "description": "",
            "created": created,
            "version": 1,
        },
        "data": {},
    }







def load_yaml_files(folder):
    """
    Διαβάζει τα YAML αρχεία και φορτώνει το επιλεγμένο στη session_state
    """

    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".yaml")])

    if not files:
        st.warning("⚠️ Ο φάκελος δεν περιέχει αρχεία YAML")
        return None, None

    selected = st.selectbox("📂 Διάλεξε αρχείο YAML", files)

    filepath = os.path.join(folder, selected)

    if st.session_state.get("current_file") != selected:
        for k in list(st.session_state.keys()):
            if "." in k:   # καθαρίζει meta.title κλπ
                del st.session_state[k]

    with open(filepath, encoding="utf-8") as f:
        st.session_state.data = yaml.safe_load(f)

    st.session_state.current_file = selected

    return st.session_state.data, filepath

def edit_yaml_data(d: dict, prefix=""):
    """
    Δημιουργεί δυναμικά inputs για YAML διατηρώντας τους τύπους
    """
    for key, value in d.items():
        widget_key = f"{prefix}{key}"

        if isinstance(value, dict):
            st.subheader(key)
            edit_yaml_data(value, prefix=widget_key + ".")

        elif isinstance(value, bool):
            d[key] = st.checkbox(key, value=value, key=widget_key)

        elif isinstance(value, int):
            d[key] = st.number_input(key, value=value, step=1, key=widget_key)

        elif isinstance(value, float):
            d[key] = st.number_input(key, value=value, key=widget_key)

        elif isinstance(value, list):
            text = "\n".join(map(str, value))
            new_value = st.text_area(
                key,
                value=text,
                key=widget_key,
                help="Ένα στοιχείο ανά γραμμή",
            )
            d[key] = [yaml.safe_load(v) for v in new_value.splitlines() if v.strip()]

        else:
            d[key] = st.text_input(key, str(value), key=widget_key)


def search_json_data(data, query, path="data"):
    results = []

    if isinstance(data, dict):
        for k, v in data.items():
            new_path = f"{path}.{k}"
            results.extend(search_json_data(v, query, new_path))

    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_path = f"{path}[{i}]"
            results.extend(search_json_data(v, query, new_path))

    else:
        if query.lower() in str(data).lower():
            results.append((path, data))

    return results

def search_in_json_folder(folder, query):
    hits = []

    for f in os.listdir(folder):
        if f.endswith(".json"):
            path = os.path.join(folder, f)
            with open(path, encoding="utf-8") as file:
                obj = json.load(file)

            results = search_json_data(obj["data"], query)

            for r in results:
                hits.append({
                    "file": f,
                    "location": r[0],
                    "value": r[1]
                })

    return hits
