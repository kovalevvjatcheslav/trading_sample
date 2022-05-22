from psycopg2 import connect
from psycopg2.extras import execute_values

from settings import settings


class DataController:
    def __init__(self):
        self.dsn = (
            f"dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER} password={settings.POSTGRES_PASSWORD} "
            f"host={settings.POSTGRES_HOST} port={settings.POSTGRES_PORT}"
        )

    def get_last_tickers_values(self):
        pass

    def save_tickers(self, tickers):
        with connect(self.dsn) as con:
            with con.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO data (ticker_name, ticker_value) VALUES %s",
                    [(f"ticker_{i}", value) for i, value in enumerate(tickers)],
                )


data_controller = DataController()
