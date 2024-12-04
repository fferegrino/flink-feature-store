from fastapi import FastAPI
import redis

redis_client = redis.Redis(host='redis', port=6379)

app = FastAPI()

@app.get("/latest_count/{restaurant_id}")
def get_latest_count(restaurant_id: int):
    return redis_client.hgetall(f'restaurant:{restaurant_id}:latest_count')
