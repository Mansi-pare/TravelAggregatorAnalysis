import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Travel Aggregator Analysis", layout="wide")
st.title("✈️ Travel Aggregator Data Analysis Dashboard")

st.markdown("This dashboard analyzes booking and session data from a travel aggregator platform.")

# --- Read CSV files directly from repo ---
@st.cache_data
def load_data():
    bookings_df = pd.read_csv("Bookings.csv")
    sessions_df = pd.read_csv("Sessions.csv")
    return bookings_df, sessions_df

try:
    bookings_df, sessions_df = load_data()
    st.success("Data loaded successfully from repository!")
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# Show the dataframes
st.subheader("📘 Bookings Data")
st.dataframe(bookings_df)

st.subheader("📗 Sessions Data")
st.dataframe(sessions_df)

st.header("📊 Analysis Results")

# 1. Distinct counts
distinct_bookings = bookings_df['booking_id'].nunique()
distinct_sessions = sessions_df['session_id'].nunique()
distinct_searches = sessions_df['search_id'].nunique()

st.subheader("1. Distinct Counts")
col1, col2, col3 = st.columns(3)
col1.metric("Distinct Bookings", distinct_bookings)
col2.metric("Distinct Sessions", distinct_sessions)
col3.metric("Distinct Searches", distinct_searches)

# 2. Bookings per destination country
st.subheader("2. Bookings by Destination Country")
fig, ax = plt.subplots()
bookings_df['destination_country'].value_counts().plot(kind='bar', ax=ax)
ax.set_title("Bookings by Country")
st.pyplot(fig)

# 3. Sessions per device type
st.subheader("3. Sessions by Device Type")
fig, ax = plt.subplots()
sessions_df['device_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
ax.set_ylabel('')
ax.set_title("Device Type Distribution")
st.pyplot(fig)

# 4. Top destination cities
st.subheader("4. Top Destination Cities")
st.write(bookings_df['destination_city'].value_counts().head(10))
