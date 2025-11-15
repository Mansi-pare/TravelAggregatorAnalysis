import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Travel Aggregator Analysis", layout="wide")
st.title("✈️ Travel Aggregator Data Analysis Dashboard")

st.markdown("Upload your `Bookings.csv` and `Sessions.csv` files to begin analysis.")

# --- File Upload ---
bookings_file = st.file_uploader("Upload Bookings.csv", type=["csv"])
sessions_file = st.file_uploader("Upload Sessions.csv", type=["csv"])

if bookings_file and sessions_file:
    bookings_df = pd.read_csv(bookings_file)
    sessions_df = pd.read_csv(sessions_file)

    st.success("Files uploaded successfully!")

    # Show the dataframes
    st.subheader("Bookings Data")
    st.dataframe(bookings_df)

    st.subheader("Sessions Data")
    st.dataframe(sessions_df)

    st.header("📊 Analysis Results")

    # 1. Distinct counts
    distinct_bookings = bookings_df['booking_id'].nunique()
    distinct_sessions = sessions_df['session_id'].nunique()
    distinct_searches = sessions_df['search_id'].nunique()

    st.subheader("1. Distinct Counts")
    st.write(f"**Distinct Bookings:** {distinct_bookings}")
    st.write(f"**Distinct Sessions:** {distinct_sessions}")
    st.write(f"**Distinct Searches:** {distinct_searches}")

    # 2. Bookings per destination country
    st.subheader("2. Bookings by Destination Country")
    fig, ax = plt.subplots()
    bookings_df['destination_country'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # 3. Sessions per device type
    st.subheader("3. Sessions by Device Type")
    fig, ax = plt.subplots()
    sessions_df['device_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

    # Example filter – show top 10 cities
    st.subheader("Top Destination Cities")
    st.write(bookings_df['destination_city'].value_counts().head(10))

else:
    st.info("Please upload both CSV files to start.")
