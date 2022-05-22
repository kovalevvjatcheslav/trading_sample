from random import random

from celery import Celery

from controller import DataController
from settings import settings

app = Celery("tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")


@app.task
def ticker_task():
    with DataController() as controller:
        tickers = controller.get_last_tickers_values()
        for ticker_name in tickers.keys():
            tickers[ticker_name] += generate_movement()
        controller.save_tickers(tickers)
        controller.publish(tickers)


app.add_periodic_task(settings.TICKER_PERIOD, ticker_task, name="ticker-task")


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == "__main__":
    app.worker_main(argv=["worker", "-B"])
