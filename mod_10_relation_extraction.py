import spacy
import os
import os
import tempfile
import pandas as pd
import streamlit as st
from pyvis.network import Network
import json 

# Φορτώνουμε το αγγλικό μοντέλο (μπορείς και για ελληνικά με το el_core_news_sm)
nlp = spacy.load("en_core_web_sm")

text = "Kyriakos Mitsotakis met with Recep Tayyip Erdogan in Athens."

doc = nlp(text)

# Βρίσκουμε οντότητες
print("Entities:")
for ent in doc.ents:
    print(ent.text, ent.label_)

print("\nPossible Relations:")
for token in doc:
    if token.pos_ == "VERB":
        subj = [w for w in token.lefts if w.dep_ in ("nsubj", "nsubjpass")]
        # ψάχνουμε και σε prepositions
        objs = [w for w in token.rights if w.dep_ in ("dobj", "pobj")]
        for obj in objs:
            # αν το obj είναι μέσα σε prep, παίρνουμε τον πραγματικό αντικείμενο
            if obj.dep_ == "pobj" and obj.head.dep_ == "prep":
                objs = [obj]
        if subj and objs:
            for o in objs:
                print(f"({subj[0].text}, {token.lemma_}, {o.text})")


#####
                
import streamlit as st
import pandas as pd
from pyvis.network import Network
import tempfile


def create_graph():

    # --- 1️⃣ Upload αρχείου ---
    uploaded_file = st.file_uploader("Choose CSV or XLS/XLSX", type=["csv","xls","xlsx"])

    if uploaded_file:
        # --- 2️⃣ Φόρτωση DataFrame ---
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Data")
        st.dataframe(df)

        # --- 3️⃣ Επιλογή στηλών για κόμβους και ακμές ---
        st.subheader("Ρυθμίσεις γράφου")
        node_columns = st.multiselect("Choose columns", options=df.columns.tolist(), default=df.columns.tolist()[:2])
        edge_columns = st.multiselect("Choose lines", options=df.columns.tolist(), default=df.columns.tolist()[2:3])
        node_color = st.color_picker("Nodes color", "#1C5AAD")
        edge_color = st.color_picker("Lines color", "#ED080F")

        # --- 4️⃣ Δημιουργία γράφου ---
        if st.button("Create graph"):
            if len(node_columns) < 2 or len(edge_columns) < 1:
                st.warning("Choose at least 2 for nodes, 1 for lines")
                st.stop()

            net = Network(height="600px", width="100%", directed=True)

            # Προσθήκη nodes
            nodes_set = set()
            for _, row in df.iterrows():
                for col in node_columns[:2]:
                    if pd.notna(row[col]) and row[col] != "":
                        nodes_set.add(row[col])
            for node in nodes_set:
                net.add_node(node, label=str(node), color=node_color)

            # Προσθήκη edges
            for _, row in df.iterrows():
                if all(pd.notna(row[col]) and row[col] != "" for col in node_columns[:2]):
                    source = str(row[node_columns[0]])
                    target = str(row[node_columns[1]])
                    edge_label = " | ".join([str(row[col]) for col in edge_columns])
                    net.add_edge(source, target, label=edge_label, color=edge_color)

            # --- 5️⃣ Εμφάνιση γράφου ---
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                net.save_graph(f.name)
                st.components.v1.html(open(f.name, "r").read(), height=600, scrolling=True)


def create_graph2(folder):

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

        # --- 3️⃣ Επιλογή στηλών για κόμβους και ακμές ---
        st.subheader("Ρυθμίσεις γράφου")
        node_columns = st.multiselect("Choose columns", options=df.columns.tolist(), default=df.columns.tolist()[:2])
        edge_columns = st.multiselect("Choose lines", options=df.columns.tolist(), default=df.columns.tolist()[2:3])
        node_color = st.color_picker("Nodes color", "#1C5AAD")
        edge_color = st.color_picker("Lines color", "#ED080F")

        # --- 4️⃣ Δημιουργία γράφου ---
        if st.button("Create graph"):
            if len(node_columns) < 2 or len(edge_columns) < 1:
                st.warning("Choose at least 2 for nodes, 1 for lines")
                st.stop()

            net = Network(height="600px", width="100%", directed=True)

            # Προσθήκη nodes
            nodes_set = set()
            for _, row in df.iterrows():
                for col in node_columns[:2]:
                    if pd.notna(row[col]) and row[col] != "":
                        nodes_set.add(row[col])
            for node in nodes_set:
                net.add_node(node, label=str(node), color=node_color)

            # Προσθήκη edges
            for _, row in df.iterrows():
                if all(pd.notna(row[col]) and row[col] != "" for col in node_columns[:2]):
                    source = str(row[node_columns[0]])
                    target = str(row[node_columns[1]])
                    edge_label = " | ".join([str(row[col]) for col in edge_columns])
                    net.add_edge(source, target, label=edge_label, color=edge_color)

            # --- 5️⃣ Εμφάνιση γράφου ---
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
                net.save_graph(f.name)
                st.components.v1.html(open(f.name, "r").read(), height=600, scrolling=True)

def create_graph_N_edges(folder: str):

    # ---------- LOAD DATA ----------
    files = [f for f in os.listdir(folder)
             if f.lower().endswith((".csv", ".xlsx", ".xls"))]

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
        else:
            df = pd.read_excel(path)

    else:
        uploaded = st.file_uploader(
            "Ανέβασε CSV ή Excel",
            type=["csv", "xlsx", "xls"]
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

    # ---------- GRAPH SETTINGS ----------
    st.subheader("Ρυθμίσεις γράφου")

    node_columns = st.multiselect(
        "Columns for nodes (source → target)",
        options=df.columns.tolist(),
        default=df.columns.tolist()[:2],
        max_selections=2
    )

    if len(node_columns) < 2:
        st.info("Επίλεξε 2 στήλες για κόμβους")
        return

    node_color = st.color_picker("Nodes color", "#1C5AAD")

    # ---------- EDGE TYPES ----------
    st.subheader("Τύποι ακμών")

    max_edge_types = len(df.columns) - 2
    n_edge_types = st.slider(
        "Πόσοι τύποι ακμών;",
        min_value=1,
        max_value=max(1, max_edge_types),
        value=2
    )

    edge_types = []

    used_columns = set(node_columns)

    for i in range(n_edge_types):
        st.markdown(f"**Edge type {i+1}**")

        available_cols = [c for c in df.columns if c not in used_columns]

        if not available_cols:
            st.warning("Δεν υπάρχουν άλλες διαθέσιμες στήλες")
            break

        col = st.selectbox(
            f"Στήλη ακμής {i+1}",
            options=available_cols,
            key=f"edge_col_{i}"
        )

        used_columns.add(col)

        color = st.color_picker(
            f"Χρώμα ακμής {i+1}",
            value="#ED080F" if i == 0 else "#1C8A3F",
            key=f"edge_color_{i}"
        )

        dashed = st.checkbox(
            f"Διακεκομμένη γραμμή (edge {i+1})",
            value=(i % 2 == 1),
            key=f"edge_dash_{i}"
        )

        edge_types.append({
            "column": col,
            "color": color,
            "dashed": dashed
        })

    # ---------- CREATE GRAPH ----------
    if st.button("Create graph"):
        net = Network(
            height="600px",
            width="100%",
            directed=True,
            bgcolor="#ffffff",
            font_color="#000000"
        )

        # --- Add nodes ---
        nodes_set = set()

        for _, row in df.iterrows():
            if all(pd.notna(row[col]) and row[col] != "" for col in node_columns):
                nodes_set.add(str(row[node_columns[0]]))
                nodes_set.add(str(row[node_columns[1]]))

        for node in nodes_set:
            net.add_node(
                node,
                label=node,
                color=node_color
            )

        # --- Add edges ---
        for _, row in df.iterrows():
            if not all(pd.notna(row[col]) and row[col] != "" for col in node_columns):
                continue

            source = str(row[node_columns[0]])
            target = str(row[node_columns[1]])

            for et in edge_types:
                col = et["column"]

                if pd.notna(row[col]) and row[col] != "":
                    net.add_edge(
                        source,
                        target,
                        label=str(row[col]),
                        color=et["color"],
                        dashes=et["dashed"],
                        title=f"Τύπος σχέσης: {col}"
                    )

        # ---------- DISPLAY ----------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            net.save_graph(f.name)
            st.components.v1.html(
                open(f.name, "r", encoding="utf-8").read(),
                height=600,
                scrolling=True
            )



def open_json(f_path):

    files = [f for f in os.listdir(f_path)
             if f.lower().endswith((".json"))]
    
    if not files:
        st.warning("no json files in the folder")
        return None

    json_file = st.selectbox("Choose a json file",
                             files
                             )
    
    json_path = os.path.join(f_path,json_file)

    try:
        with open(json_path,"r",encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error {e}")
        return None
    



def get_data(file):
    with open(file, "r") as json_file:
        data = json.load(json_file)
        return data
        

def map_algs(g, alg="barnes"):
    if alg == "barnes":
        g.barnes_hut()
    elif alg == "forced":
        g.force_atlas_2based()
    elif alg == "hr":
        g.hrepulsion()



def map_network(companies_data, alg="barnes"):
    g = Network(height="800px",width="150%")

    g.set_options("""
        {
        "nodes": {
            "shape": "box",
            "color": {
            "background": "#222222",
            "border": "#aaaaaa"
            },
            "font": {
            "color": "black"
            }
            
            
        },
        "edges": {
            "color": {
            "color": "#888888"
            }
        },
        "interaction": {
            "hover": true
        }
        }
        """)

    for company in companies_data:
        company_name = company.get("Ονομα εταιρείας")
        kladoi = company.get("Κλάδοι")

        if not company_name or not kladoi:
            continue

        # εταιρεία = node
        g.add_node(company_name, label=company_name, color="#1f77b4")

        # κάθε κλάδος = ξεχωριστό node
        for klados in kladoi.split("|"):
            klados = klados.strip()

            g.add_node(klados, label=klados, color="#ff7f0e",shape="box")
            g.add_edge(klados, company_name)

    map_algs(g, alg)
    g.write_html("companies.html")

    with open("companies.html", "r", encoding="utf-8") as f:
        html = f.read()

    st.components.v1.html(html, height=800, scrolling=True)



def map_algs2(g, alg="forced"):
    """Χρησιμοποίησε το νέο API για physics"""
    if alg == "barnes":
        g.set_options("""
        {
          "physics": {
            "enabled": true,
            "solver": "barnesHut",
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 0.3,
              "springLength": 250,
              "springConstant": 0.001,
              "damping": 0.09,
              "avoidOverlap": 0.5
            }
          }
        }
        """)
    
    elif alg == "forced":
        g.set_options("""
        {
          "physics": {
            "enabled": true,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
              "gravitationalConstant": -50,
              "centralGravity": 0.01,
              "springLength": 100,
              "springConstant": 0.08,
              "damping": 0.4,
              "avoidOverlap": 0.5
            }
          }
        }
        """)
    
    elif alg == "hr":
        g.set_options("""
        {
          "physics": {
            "enabled": true,
            "solver": "repulsion",
            "repulsion": {
              "nodeDistance": 120,
              "centralGravity": 0.0,
              "springLength": 100,
              "springConstant": 0.01,
              "damping": 0.09
            }
          }
        }
        """)


def map_network2(companies_data, alg="forced"):
    g = Network(height="800px", width="150%", directed=False)


    for company in companies_data:
        company_name = company.get("Ονομα εταιρείας")
        kladoi = company.get("Κλάδοι")

        if not company_name or not kladoi:
            continue

        tooltip = f"""
            {company_name},
            Αντικείμενο:{company.get("Αντικείμενο")},
            Κλάδοι: {company.get("Κλάδοι")},
            Κέρδη: {company.get("Κερδοφορία")}
            Σημειώσεις:
            {company.get("Σημειώσεις εταιρείες")}
            """ 

        g.add_node(
            company_name,
            label=company_name,
            title=tooltip,
            color="#1f77b4",
            shape="dot"
        )

        for klados in kladoi.split("|"):
            klados = klados.strip()
            if not klados:
                continue

            g.add_node(
                klados,
                label=klados,
                color="#ff7f0e",
                shape="box"
            )
            g.add_edge(klados, company_name)

    # ✅ physics ΠΑΝΤΑ στο τέλος
    map_algs2(g, alg)

    g.write_html("companies.html")

    with open("companies.html", "r", encoding="utf-8") as f:
        html = f.read()

        html = html.replace(
        "</html>",
        """
        <button onclick="window.print()" 
            style="position:fixed;top:10px;right:10px;z-index:99999">
            🖨 Print
        </button>
        </html>
        """
    )

    st.components.v1.html(html, height=800, scrolling=True)



