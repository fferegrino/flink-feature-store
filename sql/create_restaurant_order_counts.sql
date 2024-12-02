CREATE TABLE restaurant_order_counts (
    restaurant_id INT,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    order_count BIGINT
) WITH (
  'connector' = 'kafka',
  'topic' = 'restaurant.aggregates.order_count',
  'properties.group.id' = 'consumer-order-counts-1',
  'scan.startup.mode' = 'earliest-offset',
  'properties.bootstrap.servers' = 'broker:29092',
  'value.format' = 'json',
  'sink.partitioner' = 'fixed'
);