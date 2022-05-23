import aiopg

from settings import settings


class Db:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        dsn = (
            f"dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER} "
            f"password={settings.POSTGRES_PASSWORD} host={settings.POSTGRES_HOST} "
            f"port={settings.POSTGRES_PORT}"
        )
        self.pool = await aiopg.create_pool(dsn)

    async def create_table(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "CREATE TABLE IF NOT EXISTS data ("
                    "    id SERIAL PRIMARY KEY NOT NULL,"
                    "    ticker_name CHAR(50) NOT NULL,"
                    "    ticker_value INTEGER NOT NULL,"
                    "    created_at TIMESTAMPTZ DEFAULT Now() NOT NULL"
                    ")"
                )

    async def close_pool(self):
        self.pool.close()
        await self.pool.wait_closed()


db = Db()
