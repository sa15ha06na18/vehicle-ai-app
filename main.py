import sqlite3
import pandas as pd
import streamlit as st

# 1. Database Connection & Setup
conn = sqlite3.connect("vehicle_service.db", check_same_thread=False)
cursor = conn.cursor()

# Tables Creation
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    phone TEXT,
    email TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Vehicle (
    vehicle_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    vehicle_number TEXT,
    vehicle_model TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Service (
    service_id INTEGER PRIMARY KEY,
    vehicle_id INTEGER,
    service_type TEXT,
    service_cost REAL,
    service_date DATE
)
"""
)

conn.commit()

# Sample Data Automatic Insertion
cursor.execute("SELECT COUNT(*) FROM Customer")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO Customer VALUES (1, 'Latha', '987560958', 'latha@gmail.com')"
    )
    cursor.execute(
        "INSERT INTO Customer VALUES (2, 'Sahana', '956378399', 'sahana@gmail.com')"
    )
    cursor.execute(
        "INSERT INTO Vehicle VALUES (101, 1, 'TN37-AB-1234', 'Swift Car')"
    )
    cursor.execute(
        "INSERT INTO Vehicle VALUES (102, 2, 'TN38-CC-5678', 'City Car')"
    )
    cursor.execute(
        "INSERT INTO Service VALUES (1001, 101, 'Brake Repair', 2500, '2026-05-10')"
    )
    cursor.execute(
        "INSERT INTO Service VALUES (1002, 102, 'Oil Change', 1500, '2026-06-15')"
    )
    conn.commit()

# 2. Web UI (Streamlit Frontend)
st.title("🚗 AI-Powered Vehicle Service Management System")
st.write("Smart Database & AI Service Copilot")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    ["📊 Database View", "🤖 AI Database Copilot", "🔮 Predictive Maintenance"]
)

with tab1:
    st.subheader("Customer & Service Tables")
    st.write("### Customers")
    st.dataframe(pd.read_sql_query("SELECT * FROM Customer", conn))
    st.write("### Services History")
    st.dataframe(pd.read_sql_query("SELECT * FROM Service", conn))

with tab2:
    st.subheader("Ask AI Anything about Database")
    user_query = st.text_input(
        "Question type pannungga (e.g., Show high cost services):"
    )

    if user_query:
        if "high" in user_query.lower() or "cost" in user_query.lower():
            sql = "SELECT * FROM Service ORDER BY service_cost DESC"
        else:
            sql = "SELECT * FROM Service"

        st.info(f"Generated SQL Query: `{sql}`")
        df = pd.read_sql_query(sql, conn)
        st.write(df)

with tab3:
    st.subheader("AI Predictive Maintenance Alert")
    vehicle_sel = st.selectbox(
        "Select Vehicle Number:", ["TN37-AB-1234", "TN38-CC-5678"]
    )
    if st.button("Analyze with AI"):
        if vehicle_sel == "TN37-AB-1234":
            st.warning(
                "⚠️ AI Prediction: Brake pads worn out! Recommended service within 300 km."
            )
        else:
            st.success(
                "✅ AI Prediction: Vehicle condition good. Next oil change after 1500 km."
            )
