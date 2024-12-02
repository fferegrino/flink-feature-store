from confluent_kafka import Consumer
import json
import mysql.connector
import os

consumer = Consumer({
    'bootstrap.servers': 'broker:29092',
    'group.id': 'ingestion-group-1',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
})

consumer.subscribe(['restaurant.aggregates.order_count'])

connection = None

db_config = {
    "host": "mysql",
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DATABASE"),
}


while True:
    message = consumer.poll(1.0)
    if message is None:
        continue
    if message.error():
        print(f"Kafka error: {message.error()}")
        continue
    
    value = message.value().decode('utf-8')
    decoded_value = json.loads(value)

    try:
        connection = mysql.connector.connect(
            host=db_config.get("host"), user=db_config.get("user"), password=db_config.get("password")
        )

        if connection is not None and connection.is_connected():
            cursor = connection.cursor()

            db_name = db_config.get("database")
            connection.database = db_name

            insert_into_table_query = """INSERT INTO restaurant_order_counts (restaurant_id, window_start, window_end, order_count) VALUES (%s, %s, %s, %s)"""

            cursor.execute(insert_into_table_query, (decoded_value["restaurant_id"], decoded_value["window_start"], decoded_value["window_end"], decoded_value["order_count"]))
            connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        print(db_config)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()