from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from confluent_kafka import Consumer
import asyncio
import json

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Kafka Consumers
raw_consumer = Consumer({
    'bootstrap.servers': 'broker:29092',
    'group.id': 'frontend-raw-group-1',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
    # 'value.deserializer': lambda x: json.loads(x.decode('utf-8'))
})

raw_consumer.subscribe(['restaurant.raw.updates'])

aggregates_consumer = Consumer({
    'bootstrap.servers': 'broker:29092',
    'group.id': 'frontend-aggregates-group-1',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
    # 'value.deserializer': lambda x: json.loads(x.decode('utf-8'))
})

aggregates_consumer.subscribe(['restaurant.aggregates.order_count'])

@app.get("/", response_class=HTMLResponse)
@app.get("/map", response_class=HTMLResponse)
async def map():
    with open("static/map.html", "r") as f:
        return f.read()

@app.websocket("/aggregates")
async def aggregates_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Non-blocking check for messages from Kafka
            message = aggregates_consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print(f"Kafka error: {message.error()}")
                continue
            
            value = message.value().decode('utf-8')
            if value:
                await websocket.send_text(value)
            
            # Small delay to prevent CPU overuse
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

@app.websocket("/raw")
async def raw_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Non-blocking check for messages from Kafka
            message = raw_consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print(f"Kafka error: {message.error()}")
                continue
            
            value = message.value().decode('utf-8')
            if value:
                await websocket.send_text(value)
            
            # Small delay to prevent CPU overuse
            print(f"Sending message to websocket {value}")
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
