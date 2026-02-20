-- revenue_analysis.sql: revenue per route
SELECT route_id,
       COUNT(*) AS bookings,
       SUM(ticket_price) AS total_revenue,
       AVG(ticket_price) AS avg_price
FROM bookings
WHERE status='confirmed'
GROUP BY route_id
ORDER BY total_revenue DESC;
