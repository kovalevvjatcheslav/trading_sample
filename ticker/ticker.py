import json
from random import random

from redis import Redis
from celery import Celery

from controller import data_controller
from settings import settings

app = Celery("tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")


@app.task
def ticker_task():
    redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    tickers = redis_client.get("tickers")
    if tickers is None:
        tickers = [0] * settings.NUMBER_OF_TICKERS
    else:
        tickers = json.loads(tickers)
    try:
        # TODO: move work with redis into controller
        for i in range(len(tickers)):
            tickers[i] += generate_movement()
            redis_client.publish(f"ticker_{i}", tickers[i])
        redis_client.set("tickers", json.dumps(tickers))
        data_controller.save_tickers(tickers)
    finally:
        redis_client.close()


app.add_periodic_task(settings.TICKER_PERIOD, ticker_task, name="ticker-task")


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == "__main__":
    app.worker_main(argv=["worker", "-B"])
