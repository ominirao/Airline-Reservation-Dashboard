-- booking_metrics.sql: daily bookings and conversion
SELECT DATE(booking_timestamp) AS booking_date,
       COUNT(*) AS total_bookings,
       SUM(CASE WHEN status='confirmed' THEN 1 ELSE 0 END) AS confirmed_bookings,
       ROUND(100.0 * SUM(CASE WHEN status='confirmed' THEN 1 ELSE 0 END) / COUNT(*),2) AS conversion_pct
FROM bookings
GROUP BY DATE(booking_timestamp)
ORDER BY booking_date DESC;
