import csv
import json
import os
import random
import time
from datetime import datetime

from confluent_kafka import Producer

random.seed(0)

producer = Producer({"bootstrap.servers": "broker:29092"})

max_latitude = 19.475625
max_longitude = -99.189273
min_latitude = 19.394612
min_longitude = -99.058231

n_restaurants = 100

restaurants = []

for restaurant_id in range(n_restaurants):
    latitude = random.uniform(min_latitude, max_latitude)
    longitude = random.uniform(min_longitude, max_longitude)
    restaurants.append(
        {
            "restaurant_id": restaurant_id,
            "latitude": latitude,
            "longitude": longitude,
        }
    )

actions = ["order_received", "order_completed"]

while True:
    action = random.choice(actions)
    restaurant = random.choice(restaurants)
    action_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    message = {
        "action": action,
        "timestamp": action_time,
        **restaurant,
    }

    if action == "order_completed":
        order_completion_time = random.uniform(10.0, 30.0)
        message["order_completion_time"] = order_completion_time

    producer.produce("restaurant.updates", json.dumps(message))
    producer.poll(0)

    print(f"Produced {json.dumps(message)}")
    time.sleep(random.randint(0, 3))
