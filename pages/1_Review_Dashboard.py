import streamlit as st
import pandas as pd
import sqlite3
import os

DB_FILE = os.path.join("data", "pid_database.db")

st.set_page_config(page_title="Review Dashboard", layout="wide")
st.title("P&ID Review Dashboard")
st.write("Review items extracted by the AI that are pending approval.")

if not os.path.exists(DB_FILE):
    st.warning("Database not found. Please analyze an image on the main page first.")
else:
    conn = sqlite3.connect(DB_FILE)
    # Load data that is pending review into a pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM equipment WHERE status = 'pending_review'", conn)
    conn.close()

    if df.empty:
        st.success("///////---------No items are currently pending review!")
    else:
        st.info(f"You have {len(df)} item(s) to review.")
        st.dataframe(df)

        st.write("---")
        st.subheader("Next Steps: Build approval functionality here.")
        st.write("You can add buttons or forms to allow an engineer to 'Approve' or 'Edit' these entries, which would update their 'status' in the database.")