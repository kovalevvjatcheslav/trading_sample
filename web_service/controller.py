from sources import db


class DataController:
    @staticmethod
    async def get_all_ticker_entries(ticker_name: str) -> list[str]:
        async with db.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT created_at, ticker_value  FROM data WHERE ticker_name = %s ORDER BY created_at",
                    (ticker_name,),
                )
                return await cur.fetchall()

    @staticmethod
    async def get_ticker_names():
        async with db.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT ticker_name FROM data GROUP BY ticker_name")
                return [i[0].strip() for i in await cur.fetchall()]
