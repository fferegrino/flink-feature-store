CREATE TABLE restaurant_raw_updates (
  `restaurant_id` INT NOT NULL,
  `latitude` DOUBLE NOT NULL,
  `longitude` DOUBLE NOT NULL,
  `action` STRING NOT NULL,
  `timestamp` TIMESTAMP(3) NOT NULL,
  `order_completion_time` DOUBLE,
  WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'restaurant.updates',
  'properties.group.id' = 'consumer-group-1',
  'scan.startup.mode' = 'earliest-offset',
  'properties.bootstrap.servers' = 'broker:29092',
  'value.format' = 'json',
  'sink.partitioner' = 'fixed'
);
