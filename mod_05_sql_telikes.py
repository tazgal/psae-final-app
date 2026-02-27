import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path


def sql_connect_db(path):
    return sqlite3.connect(path)

def sql_get_tables(conn):
    q = "SELECT name FROM sqlite_master WHERE type='table'"
    return [r[0] for r in conn.execute(q).fetchall()]

def sql_get_columns(conn, table):
    q = f"PRAGMA table_info({table})"
    return [r[1] for r in conn.execute(q).fetchall()]

def sql_fetch_all(conn, table):
    return pd.read_sql_query(f"SELECT * FROM {table}", conn)

def sql_get_column_config_for_urls(df):
    config = {}
    for col in df.columns:
        if df[col].astype(str).str.startswith("http").any():
            config[col] = st.column_config.LinkColumn(col)
    return config

def sql_render_db_manager(db_path, read_only, key):

    DEFAULTS = {
        "selected_table": None,
        "action": "view_all"
    }

    for k, v in DEFAULTS.items():
        sk = f"{key}_{k}"
        if sk not in st.session_state:
            st.session_state[sk] = v


    if not Path(db_path).exists():
        st.error(f"Database not found: {db_path}")
        return

    conn = sql_connect_db(db_path)

    left_col, right_col = st.columns([4, 1], gap="small", border=True)

    with right_col:
        st.subheader("⚙️ Commands")

        tables = sql_get_tables(conn)
        table = st.selectbox(
            "📋 Select table",
            tables,
            key=f"{key}_table_select"
        )

        st.session_state[f"{key}_selected_table"] = table

        st.markdown("---")

        actions = ["view_all", "search"]
        if not read_only:
            actions.extend(["add_row", "delete_row"])

        action = st.radio(
            "Action",
            actions,
            key=f"{key}_action_radio",
            format_func=lambda x: {
                "view_all": "👁 View all",
                "search": "🔍 Search",
                "add_row": "➕ Add",
                "delete_row": "🗑 Delete"
            }[x]
        )

        st.session_state[f"{key}_action"] = action


    with left_col:
        table = st.session_state[f"{key}_selected_table"]
        action = st.session_state[f"{key}_action"]

        cols = sql_get_columns(conn, table)

        selected_columns = st.multiselect(
            "🧱 Columns to display",
            cols,
            default=cols,
            key=f"{key}_columns_select"
        )

        if not selected_columns:
            selected_columns = cols


        if action == "view_all":
            df = sql_fetch_all(conn, table)
            df = df[selected_columns]

            st.dataframe(
                df,
                use_container_width=True,
                column_config=sql_get_column_config_for_urls(df)
            )

        elif action == "search":
            search_col = st.selectbox(
                "Search column",
                cols,
                key=f"{key}_search_col"
            )

            value = st.text_input(
                "Value",
                key=f"{key}_search_value"
            )

            if value:
                q = f"SELECT * FROM {table} WHERE {search_col} LIKE ?"
                df = pd.read_sql_query(q, conn, params=[f"%{value}%"])
                df = df[selected_columns]

                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config=sql_get_column_config_for_urls(df)
                )


        elif action == "add_row":
            with st.form(f"{key}_add_form"):
                values = {
                    c: st.text_input(c, key=f"{key}_{table}_{c}")
                    for c in cols
                }

                submitted = st.form_submit_button("Save")

                if submitted:
                    keys = ", ".join(values.keys())
                    placeholders = ", ".join(["?"] * len(values))
                    q = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
                    conn.execute(q, list(values.values()))
                    conn.commit()
                    st.success("Row added")

        elif action == "delete_row":
            st.warning("⚠️ Delete is permanent")

            delete_col = st.selectbox(
                "Column (primary key)",
                cols,
                key=f"{key}_delete_col"
            )

            delete_value = st.text_input(
                "Value to delete",
                key=f"{key}_delete_value"
            )

            if delete_value:
                confirm = st.checkbox(
                    "I understand this action cannot be undone",
                    key=f"{key}_delete_confirm"
                )

                if confirm and st.button("🗑 Delete row", type="primary"):
                    q = f"DELETE FROM {table} WHERE {delete_col} = ?"
                    conn.execute(q, [delete_value])
                    conn.commit()
                    st.success("Row deleted")

import streamlit as st
import sqlite3
from pathlib import Path

# ---------- helpers ----------
DB_DIR = Path("DBs")


def connect_db(db_name: str):
    DB_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_DIR / db_name)


def create_table(conn, table_name, columns: dict):
    cols_sql = ", ".join(
        f"{name} {ctype}" for name, ctype in columns.items()
    )
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_sql})"
    conn.execute(sql)
    conn.commit()


# ---------- STREAMLIT FUNCTION ----------
def streamlit_sqlite_creator(key="db_creator"):

    left_col, right_col = st.columns([4, 1], border=True)

    # ---------------- RIGHT COLUMN ----------------
    with right_col:
        st.subheader("⚙️ DB Actions")

        run = st.button(
            "🗄️ Create / Manage DB",
            key=f"{key}_run"
        )

    # ---------------- LEFT COLUMN ----------------
    with left_col:
        st.subheader("📦 SQLite Database Manager")

        if not run:
            st.info("Press the button on the right to start")
            return

        # --- DB name ---
        db_name = st.text_input(
            "Database name",
            value="example.db",
            key=f"{key}_db_name"
        )

        # --- Table name ---
        table_name = st.text_input(
            "Table name",
            value="items",
            key=f"{key}_table_name"
        )

        st.markdown("### 🧱 Columns")

        # dynamic columns input
        col_count = st.number_input(
            "Number of columns",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            key=f"{key}_col_count"
        )

        columns = {}

        for i in range(col_count):
            c1, c2 = st.columns(2)
            with c1:
                col_name = st.text_input(
                    f"Column {i+1} name",
                    key=f"{key}_col_name_{i}"
                )
            with c2:
                col_type = st.selectbox(
                    f"Column {i+1} type",
                    [
                        "TEXT",
                        "INTEGER",
                        "REAL",
                        "INTEGER PRIMARY KEY AUTOINCREMENT"
                    ],
                    key=f"{key}_col_type_{i}"
                )

            if col_name:
                columns[col_name] = col_type

        if not columns:
            st.warning("Define at least one column")
            return

        # --- EXECUTION ---
        if st.button("🚀 Execute", key=f"{key}_execute"):
            conn = connect_db(db_name)
            create_table(conn, table_name, columns)

            st.success(f"Database `{db_name}` updated")
            st.code(
                f"CREATE TABLE {table_name} ({columns})",
                language="sql"
            )
