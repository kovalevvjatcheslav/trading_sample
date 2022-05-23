from contextlib import AbstractContextManager
from datetime import datetime
import json
from typing import Dict

from psycopg2 import connect
from psycopg2.extras import execute_values
from redis import Redis

from settings import settings


class DateTimeEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        else:
            return super().default(value)


class DataController(AbstractContextManager):
    def __init__(self):
        self.dsn = (
            f"dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER} password={settings.POSTGRES_PASSWORD} "
            f"host={settings.POSTGRES_HOST} port={settings.POSTGRES_PORT}"
        )
        self.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis.close()

    def get_last_tickers_values(self) -> Dict[str, tuple[datetime, int]]:
        tickers = self.redis.get("tickers")
        if tickers is None:
            with connect(self.dsn) as con:
                with con.cursor() as cur:
                    cur.execute(
                        "SELECT d.ticker_name, mx.created_at, mx.ticker_value "
                        "FROM ("
                        "   SELECT ticker_name, max(created_at) as max_created_at FROM data GROUP BY ticker_name"
                        ") d "
                        "INNER JOIN data mx ON mx.created_at = d.max_created_at AND mx.ticker_name = d.ticker_name"
                    )
                    tickers = {
                        ticker_name: (created_at, ticker_value)
                        for ticker_name, created_at, ticker_value in cur.fetchall()
                    }
        else:
            tickers = json.loads(tickers)
        if tickers == {}:
            now = datetime.utcnow()
            tickers = {f"ticker_{i}": (now, 0) for i in range(settings.NUMBER_OF_TICKERS)}
        return tickers

    def save_tickers(self, tickers: Dict[str, tuple[datetime, int]]):
        with connect(self.dsn) as con:
            with con.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO data (ticker_name, created_at, ticker_value) VALUES %s",
                    [
                        (ticker_name, ticker_data[0], ticker_data[1])
                        for ticker_name, ticker_data in tickers.items()
                    ],
                )
        self.redis.set("tickers", json.dumps(tickers, cls=DateTimeEncoder))

    def publish(self, tickers: Dict[str, tuple[datetime, int]]):
        for ticker_name, ticker_data in tickers.items():
            self.redis.publish(ticker_name, json.dumps(ticker_data, cls=DateTimeEncoder))
