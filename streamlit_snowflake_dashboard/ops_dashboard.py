import streamlit as st
from snowflake.snowpark.context import get_active_session

# Page config
st.set_page_config(layout="wide")
st.title("GTM Operations Dashboard")
st.markdown("Built natively in Snowflake (SiS) to explore the architecture!")
st.divider()

# Get snowflake session
session = get_active_session()

# Query to fetch high level metrics with sample data
metrics_query = """
    SELECT 
        COUNT(O_ORDERKEY) as TOTAL_ORDERS,
        SUM(O_TOTALPRICE) as TOTAL_REVENUE
    FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
"""
df_metrics = session.sql(metrics_query).to_pandas()

# Display Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Orders (All Time)", value=f"{df_metrics['TOTAL_ORDERS'][0]:,}")
with col2:
    st.metric(label="Total Revenue ($)", value=f"${df_metrics['TOTAL_REVENUE'][0]:,.2f}")

st.divider()

# Quwry to fetch and display orders by status
st.subheader("Order Pipeline Status")
status_query = """
    SELECT 
        O_ORDERSTATUS as STATUS, 
        COUNT(O_ORDERKEY) as ORDER_COUNT 
    FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS 
    GROUP BY O_ORDERSTATUS
"""
df_status = session.sql(status_query).to_pandas()

# Show a bar chart
st.bar_chart(data=df_status, x="STATUS", y="ORDER_COUNT")

# Show Raw Data Toggle
if st.checkbox("Show Raw Data Table"):
    st.dataframe(df_status)
