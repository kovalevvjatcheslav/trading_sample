import json
from random import random

from redis import Redis
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'ticker-task': {
        'task': 'ticker.ticker_task',
        'schedule': 5,
    },
}


@app.task
def ticker_task():
    redis_client = Redis(host='localhost', port=6379, db=0)
    tickers = redis_client.get("tickers")
    if tickers is None:
        tickers = [0]*5
    else:
        tickers = json.loads(tickers)
    try:
        for i in range(len(tickers)):
            tickers[i] += generate_movement()
            redis_client.publish(f"ticker_{i}", tickers[i])
        redis_client.set("tickers", json.dumps(tickers))
    finally:
        redis_client.close()


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement
