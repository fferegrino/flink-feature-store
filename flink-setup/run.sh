#! /bin/bash

cat /queries/create_restaurant_raw_updates.sql >> /tmp/queries.sql
cat /queries/create_restaurant_order_counts.sql >> /tmp/queries.sql
cat /queries/insert_restaurant_order_counts.sql >> /tmp/queries.sql

./bin/sql-client.sh -f /tmp/queries.sql

echo "Done"
