from contextlib import AbstractContextManager
import json
from typing import Dict

from psycopg2 import connect
from psycopg2.extras import execute_values
from redis import Redis

from settings import settings


class DataController(AbstractContextManager):
    def __init__(self):
        self.dsn = (
            f"dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER} password={settings.POSTGRES_PASSWORD} "
            f"host={settings.POSTGRES_HOST} port={settings.POSTGRES_PORT}"
        )
        self.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis.close()

    def get_last_tickers_values(self) -> Dict[str, int]:
        tickers = self.redis.get("tickers")
        if tickers is None:
            with connect(self.dsn) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "SELECT d.ticker_name, mx.ticker_value "
                        "FROM ("
                        "   SELECT ticker_name, max(created_at) as max_created_at FROM data GROUP BY ticker_name"
                        ") d "
                        "INNER JOIN data mx ON mx.created_at = d.max_created_at AND mx.ticker_name = d.ticker_name"
                    )
                    tickers = {ticker_name: ticker_value for ticker_name, ticker_value in cur.fetchall()}
        else:
            tickers = json.loads(tickers)
        if tickers == {}:
            tickers = {f"ticker_{i}": 0 for i in range(settings.NUMBER_OF_TICKERS)}
        return tickers

    def save_tickers(self, tickers: Dict[str, int]):
        with connect(self.dsn) as con:
            with con.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO data (ticker_name, ticker_value) VALUES %s",
                    [(ticker_name, value) for ticker_name, value in tickers.items()],
                )
        self.redis.set("tickers", json.dumps(tickers))

    def publish(self, tickers: Dict[str, int]):
        for ticker_name, ticker_value in tickers.items():
            self.redis.publish(ticker_name, ticker_value)
