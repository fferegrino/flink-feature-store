from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from confluent_kafka import Consumer
import asyncio
import json

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'broker:29092',
    'group.id': 'frontend-group-1',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
    # 'value.deserializer': lambda x: json.loads(x.decode('utf-8'))
})

consumer.subscribe(['restaurant.updates'])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Non-blocking check for messages from Kafka
            message = consumer.poll(1.0)
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
