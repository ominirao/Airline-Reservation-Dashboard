import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

st.set_page_config(page_title="Airline Reservation Dashboard", layout="wide")
st.title("Airline Reservation — Business Analytics Dashboard")

DB_PATH = "airline_demo.db"

# Connect to database
try:
    conn = sqlite3.connect(DB_PATH)
    bookings = pd.read_sql("SELECT * FROM bookings", conn, parse_dates=["booking_timestamp"])
except Exception as e:
    st.error("Database not found or invalid.")
    st.stop()

# -------------------------
# KPIs
# -------------------------
st.markdown("## Key Metrics")

total_bookings = len(bookings)
confirmed = (bookings['status'] == "confirmed").sum()
cancelled = (bookings['status'] == "cancelled").sum()
conversion_rate = round(100 * confirmed / total_bookings, 2) if total_bookings else 0
revenue = bookings.loc[bookings['status']=="confirmed", 'ticket_price'].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Bookings", f"{total_bookings:,}")
k2.metric("Confirmed", f"{confirmed:,}")
k3.metric("Cancelled", f"{cancelled:,}")
k4.metric("Revenue", f"${revenue:,.2f}")

# -------------------------
# Booking Trend
# -------------------------
st.markdown("## Booking Trend")

bookings['booking_date'] = bookings['booking_timestamp'].dt.date
trend = bookings.groupby('booking_date').size().reset_index(name="count")
st.line_chart(trend.set_index("booking_date"))

# -------------------------
# Revenue by Route
# -------------------------
st.markdown("## Revenue by Route")

route_revenue = bookings[bookings['status']=="confirmed"].groupby("route_id").agg(
    bookings=("booking_id","count"),
    total_revenue=("ticket_price","sum"),
    avg_price=("ticket_price","mean")
).reset_index().sort_values("total_revenue", ascending=False)

st.dataframe(route_revenue)

# -------------------------
# Sample Data
# -------------------------
st.markdown("## Sample Bookings")
st.dataframe(bookings.head(20))

st.download_button(
    "Download Bookings CSV",
    bookings.to_csv(index=False).encode("utf-8"),
    "bookings.csv"
)