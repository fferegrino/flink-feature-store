import csv
import os
import time

from confluent_kafka.admin import AdminClient, NewTopic
import mysql.connector
from confluent_kafka.admin import AdminClient, NewTopic
from mysql.connector import Error

# Create topics
kafka_admin = AdminClient({"bootstrap.servers": "broker:9092"})

topics = [
    "restaurant.raw.updates",
    "restaurant.aggregates.order_count",
]

existing_topics = set(kafka_admin.list_topics().topics)

for topic in topics:
    new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)

    if topic not in existing_topics:
        kafka_admin.create_topics([new_topic])
        print(f"Topic {topic} created successfully.")
    else:
        print(f"Topic {topic} already exists.")

# Setup database
connection = None

db_config = {
    "host": "mysql",
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DATABASE"),
}

try:
    connection = mysql.connector.connect(
        host=db_config.get("host"), user=db_config.get("user"), password=db_config.get("password")
    )

    if connection is not None and connection.is_connected():
        cursor = connection.cursor()

        db_name = db_config.get("database")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully.")

        connection.database = db_name

        create_table_query = """
CREATE TABLE restaurant_order_counts (
  restaurant_id INT,
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  order_count BIGINT,
  PRIMARY KEY (restaurant_id, window_end)
);"""

        cursor.execute(create_table_query)

        connection.commit()

except Error as e:
    print(f"Error: {e}")
    print(db_config)
finally:
    if connection is not None and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")