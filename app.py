import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Airline Reservation Dashboard", layout="wide")
st.title("Airline Reservation — Business Analytics Dashboard")

DB_PATH = "airline_demo.db"

# Connect to DB
try:
    conn = sqlite3.connect(DB_PATH)
    bookings = pd.read_sql("SELECT * FROM bookings", conn, parse_dates=["booking_timestamp"])
except Exception as e:
    st.error("Database not found or invalid. Make sure airline_demo.db is in the repo root.")
    st.stop()

# KPIs
st.markdown("## Key Metrics")
total_bookings = len(bookings)
confirmed = (bookings['status'] == "confirmed").sum() if 'status' in bookings.columns else 0
cancelled = (bookings['status'] == "cancelled").sum() if 'status' in bookings.columns else 0
conversion_rate = round(100 * confirmed / total_bookings, 2) if total_bookings else 0
revenue = bookings.loc[bookings['status']=="confirmed", 'ticket_price'].sum() if 'ticket_price' in bookings.columns else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Bookings", f"{total_bookings:,}")
c2.metric("Confirmed", f"{confirmed:,}")
c3.metric("Cancelled", f"{cancelled:,}")
c4.metric("Revenue", f"${revenue:,.2f}")

# Trend
st.markdown("## Booking Trend")
bookings['booking_date'] = bookings['booking_timestamp'].dt.date
trend = bookings.groupby('booking_date').size().reset_index(name="count")
st.line_chart(trend.set_index("booking_date"))

# Revenue by route
st.markdown("## Revenue by Route (confirmed)")
if 'route_id' in bookings.columns and 'ticket_price' in bookings.columns:
    rev = bookings[bookings['status']=="confirmed"].groupby("route_id").agg(
        bookings=("booking_id","count"),
        total_revenue=("ticket_price","sum"),
        avg_price=("ticket_price","mean")
    ).reset_index().sort_values("total_revenue", ascending=False)
    st.dataframe(rev)
else:
    st.write("No route_id or ticket_price to compute revenue.")

# Sample bookings
st.markdown("## Sample bookings")
st.dataframe(bookings.head(20))

# Download
st.download_button("Download bookings CSV", bookings.to_csv(index=False).encode("utf-8"), "bookings.csv")
