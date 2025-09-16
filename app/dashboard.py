import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Delivery Ops Command Center", layout="wide")

st.title("Delivery Ops Command Center")
st.caption("MVP dashboard — replace with real marts and model metrics.")

col1, col2, col3 = st.columns(3)
col1.metric("On-time % (mock)", "92.4", "+0.8")
col2.metric("Avg Duration (min)", "14.7", "-0.4")
col3.metric("Anomalies (7d)", "36", "↔")

st.subheader("Trips by Hour (mock)")
hours = np.arange(24)
counts = (np.sin(hours/3) + 1.2) * 100 + np.random.randint(0, 20, 24)
st.bar_chart(pd.DataFrame({"trips": counts}, index=hours))

st.info("Connect this to dbt feature marts in later days.")
