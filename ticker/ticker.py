import json
from random import random

from redis import Redis

from celery import Celery

app = Celery('tasks', broker='redis://redis:6379/0')


@app.task
def ticker_task():
    redis_client = Redis(host='redis', port=6379, db=0)
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


app.add_periodic_task(5, ticker_task, name="ticker-task")


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == "__main__":
    app.worker_main(argv=["worker", "-B"])
