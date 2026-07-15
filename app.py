import streamlit as st
import pandas as pd
import json

# Page configuration
st.set_page_config(page_title="Instant DB Normalizer Pro", page_icon="⚡", layout="wide")

st.title("⚡ Instant Automated 3NF Database Normalizer")
st.write("Enter a flat data record and its rules to watch it instantly split into a normalized schema with raw SQL export.")

# --- SIDEBAR: STEP 1 (User Input) ---
st.sidebar.header("Step 1: Define Raw Record & Rules")

# Default input data for quick testing
default_record = '{"StudentID": "101", "StudentName": "Alice", "CourseID": "CS101", "CourseName": "Intro to CS", "Grade": "A"}'
default_fds = 'StudentID -> StudentName\nCourseID -> CourseName\nStudentID, CourseID -> Grade'

raw_record_input = st.sidebar.text_area("1. Paste Single Record (JSON Format):", value=default_record, height=110)
fds_input = st.sidebar.text_area("2. Enter Functional Dependencies (one per line):", value=default_fds, height=110)

# --- ENGINE: STEP 2 (Processing Logic) ---
def parse_inputs(record_str, fds_str):
    try:
        record = json.loads(record_str)
    except Exception:
        st.error("❌ Invalid JSON format in the record field.")
        return None, None

    fds = []
    for line in fds_str.strip().split("\n"):
        if "->" in line:
            lhs, rhs = line.split("->")
            lhs_cols = [c.strip() for c in lhs.split(",") if c.strip()]
            rhs_cols = [c.strip() for c in rhs.split(",") if c.strip()]
            fds.append({"LHS": lhs_cols, "RHS": rhs_cols})
    
    return record, fds

def generate_sql_scripts(t_name, pk_cols, all_cols, record):
    # Construct CREATE TABLE
    columns_sql = []
    for col in all_cols:
        val = record.get(col, "")
        # Basic type inference
        col_type = "INT" if str(val).isdigit() else "VARCHAR(255)"
        columns_sql.append(f"    {col} {col_type}")
    
    pk_string = ", ".join(pk_cols)
    columns_sql.append(f"    PRIMARY KEY ({pk_string})")
    create_sql = f"CREATE TABLE {t_name} (\n" + ",\n".join(columns_sql) + "\n);"

    # Construct INSERT INTO
    insert_cols = ", ".join(all_cols)
    insert_vals = []
    for col in all_cols:
        val = record.get(col, "")
        if str(val).isdigit():
            insert_vals.append(str(val))
        else:
            # Escape single quotes
            clean_val = str(val).replace("'", "''")
            insert_vals.append(f"'{clean_val}'")
    
    vals_string = ", ".join(insert_vals)
    insert_sql = f"INSERT INTO {t_name} ({insert_cols})\nVALUES ({vals_string});"
    
    return f"{create_sql}\n\n{insert_sql}"

def normalize_to_3nf(record, fds):
    normalized_tables = {}
    
    for index, fd in enumerate(fds):
        table_name = f"tbl_{'_'.join(fd['LHS']).lower()}"
        primary_keys = fd["LHS"]
        dependent_attributes = fd["RHS"]
        all_columns = primary_keys + dependent_attributes
        
        table_data = {col: [record[col]] for col in all_columns if col in record}
        
        if table_data:
            df = pd.DataFrame(table_data)
            sql_script = generate_sql_scripts(table_name, primary_keys, all_columns, record)
            
            normalized_tables[table_name] = {
                "Primary_Keys": primary_keys,
                "DataFrame": df,
                "SQL": sql_script
            }
            
    return normalized_tables

# --- MAIN UI: STEP 3 (Display Output) ---
record, fds = parse_inputs(raw_record_input, fds_input)

if record and fds:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Input Raw Flattened Record")
        st.json(record)
        
        st.subheader("⛓️ Detected Dependencies")
        for fd in fds:
            st.code(f"{', '.join(fd['LHS'])} ➔ {', '.join(fd['RHS'])}")

    with col2:
        st.subheader("🗂️ Auto-Generated 3NF Schema")
        
        normalized_results = normalize_to_3nf(record, fds)
        
        all_sql_scripts = []
        for t_name, t_info in normalized_results.items():
            all_sql_scripts.append(t_info["SQL"])
            
            with st.container(border=True):
                st.markdown(f"### 📋 {t_name.upper()}")
                st.markdown(f"**Primary Key(s):** `{', '.join(t_info['Primary_Keys'])}`")
                
                # Render the row data as a dataframe
                st.dataframe(t_info["DataFrame"], use_container_width=True, hide_index=True)
                
                # Show SQL code tab inside the container
                with st.expander("🔍 View Table SQL"):
                    st.code(t_info["SQL"], language="sql")

        # Master SQL Download Button at the bottom
        st.write("---")
        st.subheader("💾 Export Full DDL")
        full_sql_output = "\n\n-- =========================================\n\n".join(all_sql_scripts)
        st.download_button(
            label="📥 Download Complete .SQL Script",
            data=full_sql_output,
            file_name="normalized_schema.sql",
            mime="text/plain",
            use_container_width=True
        )