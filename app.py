import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Travel Aggregator Analysis", layout="wide")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    bookings = pd.read_csv("bookings.csv")
    sessions = pd.read_csv("sessions.csv")
    return bookings, sessions


bookings_df, sessions_df = load_data()

st.title("✈️ Travel Aggregator Data Analysis Dashboard")
st.write("Explore customer bookings, sessions, trends, insights, and KPIs.")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "Select Destination City (to_city)",
    options=sorted(bookings_df["to_city"].unique()),
    default=None
)

service_filter = st.sidebar.multiselect(
    "Select Service Name",
    options=sorted(bookings_df["service_name"].unique()),
    default=None
)

filtered_bookings = bookings_df.copy()

if city_filter:
    filtered_bookings = filtered_bookings[filtered_bookings["to_city"].isin(city_filter)]

if service_filter:
    filtered_bookings = filtered_bookings[filtered_bookings["service_name"].isin(service_filter)]


# -------------------------
# OVERVIEW STATISTICS
# -------------------------
st.header("📊 Key Performance Indicators (KPIs)")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Bookings", len(filtered_bookings))

with col2:
    st.metric("Total Revenue (INR)", f"{filtered_bookings['INR_Amount'].sum():,.2f}")

with col3:
    st.metric("Average Ticket Price", f"{filtered_bookings['INR_Amount'].mean():,.2f}")


# -------------------------
# CUSTOMER BOOKING SEARCH
# -------------------------
st.header("🔍 Search Customer Booking Details")

search_customer = st.text_input("Enter Customer ID to Search")

if search_customer:
    result = bookings_df[bookings_df["customer_id"].astype(str) == search_customer]

    if not result.empty:
        st.success(f"Found {len(result)} bookings for Customer ID: {search_customer}")
        st.dataframe(result)
    else:
        st.error("No bookings found for this Customer ID.")


# -------------------------
# VISUALIZATIONS
# -------------------------
st.header("📈 Visual Insights")

# 1. Device Type Chart (corrected — uses bookings_df)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📱 Device Type Used (Bookings Data)")

    fig1, ax1 = plt.subplots()
    bookings_df["device_type_used"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax1)
    ax1.set_ylabel("")
    st.pyplot(fig1)

# 2. Service Usage Chart
with col2:
    st.subheader("🛎️ Service Usage Distribution")

    fig2, ax2 = plt.subplots()
    bookings_df["service_name"].value_counts().plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Service Name")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)


# 3. Booking Trend Over Time
st.subheader("📅 Bookings Over Time")

bookings_df["booking_time"] = pd.to_datetime(bookings_df["booking_time"])
bookings_time_series = bookings_df.groupby(bookings_df["booking_time"].dt.date).size()

fig3, ax3 = plt.subplots()
bookings_time_series.plot(ax=ax3)
ax3.set_xlabel("Date")
ax3.set_ylabel("Number of Bookings")
st.pyplot(fig3)


# 4. INR Amount vs Distance
st.subheader("💸 INR Amount vs Distance (km)")

fig4, ax4 = plt.subplots()
ax4.scatter(bookings_df["distance_km"], bookings_df["INR_Amount"])
ax4.set_xlabel("Distance (km)")
ax4.set_ylabel("INR Amount")
st.pyplot(fig4)


# -------------------------
# SESSION ANALYSIS
# -------------------------
st.header("🧭 User Session Analysis")

st.write(f"Total Sessions: {len(sessions_df)}")

st.write("### Sessions Data Overview")
st.dataframe(sessions_df.head())


# -------------------------
# DAYS TO DEPARTURE ANALYSIS
# -------------------------
st.header("⏳ Impact of Days-to-Departure on Fare")

fig5, ax5 = plt.subplots()
ax5.scatter(bookings_df["days_to_departure"], bookings_df["INR_Amount"])
ax5.set_xlabel("Days to Departure")
ax5.set_ylabel("INR Amount")
st.pyplot(fig5)


# -------------------------
# END OF APP
# -------------------------
st.write("---")
st.write("Built by Mansi Pare 🌟 | Travel Aggregator Internship Project Dashboard")
