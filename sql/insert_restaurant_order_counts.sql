INSERT INTO restaurant_order_counts
SELECT
    restaurant_id,
    window_start,
    window_end,
    count(*) AS order_count
FROM TABLE(
    HOP(TABLE restaurant_raw_updates, DESCRIPTOR(`timestamp`), INTERVAL '1' MINUTE, INTERVAL '10' MINUTES))
WHERE action = 'order_completed'
GROUP BY
    restaurant_id,
    window_start,
    window_end;
