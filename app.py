import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Travel Aggregator Analysis", layout="wide")
st.title("✈️ Travel Aggregator Data Analysis Dashboard")

st.markdown("Analyze bookings and sessions data interactively. Use filters, search tools, and calculators.")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    bookings_df = pd.read_csv("Bookings.csv")
    sessions_df = pd.read_csv("Sessions.csv")
    return bookings_df, sessions_df

try:
    bookings_df, sessions_df = load_data()
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -------------------------
# Show raw data (Collapsible)
# -------------------------
with st.expander("📘 View Raw Bookings Data"):
    st.dataframe(bookings_df)

with st.expander("📗 View Raw Sessions Data"):
    st.dataframe(sessions_df)

st.write("---")

# ======================================================
# 1️⃣ CUSTOMER LOOKUP TOOL
# ======================================================
st.header("🔍 Customer Lookup Tool")

customer_id_input = st.text_input("Enter Customer ID:")

if customer_id_input:
    customer_data = bookings_df[bookings_df["customer_id"] == customer_id_input]

    if not customer_data.empty:
        st.success("Customer found!")
        st.subheader("📄 Customer Booking Details")
        st.dataframe(customer_data)

        total_spent = customer_data["INR_Amount"].sum()
        st.metric("Total Amount Spent (INR)", total_spent)
    else:
        st.error("No data found for this customer ID.")

st.write("---")

# ======================================================
# 2️⃣ BOOKING COST ESTIMATOR
# ======================================================
st.header("💰 Booking Cost Estimator")

colA, colB, colC = st.columns(3)

distance_km = colA.number_input("Distance (km)", min_value=1, value=500)
passengers = colB.number_input("Number of Passengers", min_value=1, value=1)
service_type = colC.selectbox("Service Type", ["Flight", "Train", "Bus"])

# Base rates
rates = {"Flight": 6.5, "Train": 2.2, "Bus": 1.4}

if st.button("Calculate Estimated Cost"):
    cost = distance_km * rates[service_type] * passengers
    st.success(f"Estimated Booking Cost: **₹{round(cost, 2)}**")

st.write("---")

# ======================================================
# 3️⃣ DYNAMIC FILTERS
# ======================================================
st.header("🎛 Dynamic Filters for Exploration")

cities = sorted(bookings_df["to_city"].dropna().unique())
countries = sorted(bookings_df["to_country"].dropna().unique())

col1, col2 = st.columns(2)
selected_city = col1.selectbox("Select Destination City", ["All"] + cities)
selected_country = col2.selectbox("Select Destination Country", ["All"] + countries)

filtered_df = bookings_df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["to_city"] == selected_city]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["to_country"] == selected_country]

st.subheader("📌 Filtered Results")
st.dataframe(filtered_df)

st.write("---")

# ======================================================
# 4️⃣ AUTO INSIGHTS SECTION
# ======================================================
st.header("✨ Automatic Insights")

try:
    most_city = bookings_df["to_city"].value_counts().idxmax()
    most_device = sessions_df["device_type_used"].value_counts().idxmax()
    avg_distance = round(bookings_df["distance_km"].mean(), 2)
    highest_pay_user = bookings_df.groupby("customer_id")["INR_Amount"].sum().idxmax()
except:
    most_city = most_device = avg_distance = highest_pay_user = "Not available"

st.markdown(f"""
- 🌍 **Most booked destination city:** {most_city}  
- 📱 **Most used device type:** {most_device}  
- 🚗 **Average travel distance:** {avg_distance} km  
- 👤 **Highest paying customer:** {highest_pay_user}  
""")

st.write("---")

# ======================================================
# 5️⃣ VISUALIZATIONS
# ======================================================
st.header("📊 Visualizations")

# --- Bookings by Destination Country ---
st.subheader("📌 Bookings by Destination Country")
fig1, ax1 = plt.subplots()
bookings_df["to_country"].value_counts().plot(kind="bar", ax=ax1)
ax1.set_title("Bookings by Country")
st.pyplot(fig1)

# --- Device Type Distribution ---
st.subheader("📱 Sessions by Device Type")
fig2, ax2 = plt.subplots()
sessions_df["device_type_used"].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax2)
ax2.set_ylabel("")
ax2.set_title("Device Type Distribution")
st.pyplot(fig2)

# --- Top 10 Destination Cities ---
st.subheader("🏙 Top Destination Cities")
st.table(bookings_df["to_city"].value_counts().head(10))

st.write("✔ Dashboard Loaded Successfully")
