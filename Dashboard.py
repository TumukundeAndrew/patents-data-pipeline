import streamlit as st
import pandas as pd
import json

# Set page configuration
st.set_page_config(page_title="Patents Dashboard", page_icon="📜", layout="wide")

st.title("📜 Patents Data Dashboard")
# st.markdown("A simple dashboard summarizing the top entities in the USPTO Patents Database.")

# Load data
try:
    with open("summary_report.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Error: summary_report.json not found. Please run the data pipeline first.")
    st.stop()

# 1. Key Metrics
st.header("Overview")
st.metric(label="Total Patents Processed", value=f"{data.get('total_patents', 0):,}")

st.markdown("---")

col1, col2 = st.columns(2)

# 2. Top Companies
with col1:
    st.subheader("🏢 Top 5 Companies")
    companies_df = pd.DataFrame(data.get('top_companies', []))
    if not companies_df.empty:
        # Display Bar Chart
        st.bar_chart(companies_df.set_index('name')['patents'])
        # Display Table
        st.dataframe(companies_df.rename(columns={'name': 'Company', 'patents': 'Patents'}), use_container_width=True)
    else:
        st.write("No company data available.")

# 3. Top Inventors
with col2:
    st.subheader("💡 Top 5 Inventors")
    inventors_df = pd.DataFrame(data.get('top_inventors', []))
    if not inventors_df.empty:
        # Display Bar Chart
        st.bar_chart(inventors_df.set_index('name')['patents'])
        # Display Table
        st.dataframe(inventors_df.rename(columns={'name': 'Inventor', 'patents': 'Patents'}), use_container_width=True)
    else:
        st.write("No inventor data available.")

st.markdown("---")

# 4. Top Countries
st.subheader("🌍 Top 5 Countries by Patent Share")
countries_df = pd.DataFrame(data.get('top_countries', []))
if not countries_df.empty:
    # Convert share to percentage for better readability
    countries_df['Share (%)'] = (countries_df['share'] * 100).round(2)
    
    col_country_chart, col_country_table = st.columns([2, 1])
    
    with col_country_chart:
        st.bar_chart(countries_df.set_index('country')['Share (%)'])
        
    with col_country_table:
        st.dataframe(countries_df[['country', 'Share (%)']].rename(columns={'country': 'Country'}), use_container_width=True)
else:
    st.write("No country data available.")

st.markdown("---")
st.caption("Dashboard built with Streamlit based on 100,000 USPTO patent records.")
