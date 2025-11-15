import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Travel Aggregator Analysis", layout="wide")
st.title("✈️ Travel Aggregator Data Analysis Dashboard")

st.markdown("This dashboard analyzes booking and session data from a travel aggregator platform.")

# --- Read CSV files from repo ---
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

# Show data
st.subheader("📘 Bookings Data")
st.dataframe(bookings_df)

st.subheader("📗 Sessions Data")
st.dataframe(sessions_df)

st.header("📊 Analysis Results")

# --- 1. Distinct Counts ---
distinct_bookings = bookings_df['booking_id'].nunique()
distinct_sessions = sessions_df['session_id'].nunique()
distinct_searches = sessions_df['search_id'].nunique()

st.subheader("1. Distinct Counts")
col1, col2, col3 = st.columns(3)
col1.metric("Distinct Bookings", distinct_bookings)
col2.metric("Distinct Sessions", distinct_sessions)
col3.metric("Distinct Searches", distinct_searches)

# --- 2. Bookings per Destination Country (to_country) ---
st.subheader("2. Bookings by Destination Country")
fig, ax = plt.subplots()
bookings_df['to_country'].value_counts().plot(kind='bar', ax=ax)
ax.set_title("Bookings by Destination Country")
ax.set_xlabel("Country")
ax.set_ylabel("Count")
st.pyplot(fig)

# --- 3. Device Type Usage (from bookings file) ---
st.subheader("3. Device Type Distribution")
fig, ax = plt.subplots()
bookings_df['device_type_used'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
ax.set_ylabel('')
ax.set_title("Device Type Used")
st.pyplot(fig)

# --- 4. Top Destination Cities ---
st.subheader("4. Top Destination Cities")
top_cities = bookings_df['to_city'].value_counts().head(10)
st.write(top_cities)

fig, ax = plt.subplots()
top_cities.plot(kind='bar', ax=ax)
ax.set_title("Top 10 Destination Cities")
ax.set_xlabel("City")
ax.set_ylabel("Count")
st.pyplot(fig)
