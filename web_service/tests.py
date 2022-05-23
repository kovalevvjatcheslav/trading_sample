from datetime import datetime
from time import sleep
import unittest

from httpx import AsyncClient
from fastapi.testclient import TestClient
from redis import Redis

from main import app
from settings import settings
from sources import db


class TestAPI(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await db.create_pool()
        await db.create_table()
        self.http_client = AsyncClient(app=app, base_url="http://test")
        self.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    async def asyncTearDown(self):
        async with db.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "DROP TABLE IF EXISTS data",
                )
        await db.close_pool()

    @staticmethod
    async def _add_ticker_data():
        async with db.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO data (ticker_name, ticker_value, created_at) VALUES %s, %s, %s",
                    [
                        ("ticker_0", 42, datetime(2022, 1, 2, 20, 5, 10)),
                        ("ticker_0", 1, datetime(1984, 1, 2, 20, 5, 10)),
                        ("ticker_2", 213, datetime(1585, 1, 2, 20, 5, 10)),
                    ],
                )

    async def test_root(self):
        response = await self.http_client.get("/")
        self.assertEqual(response.status_code, 200)

    async def test_get_ticker_entries(self):
        await self._add_ticker_data()
        response = await self.http_client.get("/ticker_entries/ticker_0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), [["1984-01-02T20:05:10+00:00", 1], ["2022-01-02T20:05:10+00:00", 42]]
        )

    def test_get_realtime(self):
        ws_client = TestClient(app)
        with ws_client.websocket_connect("/realtime_data/ticker_1") as websocket:
            sleep(1)
            self.redis.publish("ticker_1", 42)
            data = websocket.receive_json()
            websocket.exit_stack.pop_all()
        self.assertEqual(data, 42)


if __name__ == "__main__":
    unittest.main()
