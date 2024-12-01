import csv
import os
import time

from confluent_kafka.admin import AdminClient, NewTopic

kafka_admin = AdminClient({"bootstrap.servers": "broker:9092"})

topics = [
    "restaurant.updates",
]

existing_topics = set(kafka_admin.list_topics().topics)

for topic in topics:
    new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)

    if topic not in existing_topics:
        kafka_admin.create_topics([new_topic])
        print(f"Topic {topic} created successfully.")
    else:
        print(f"Topic {topic} already exists.")
