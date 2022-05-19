from sources import db


class DataController:
    @staticmethod
    async def get_all_ticker_entries(ticker_name):
        async with db.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT ticker_value, created FROM data WHERE ticker_name = %s ORDER BY created", (ticker_name,)
                )
                return await cur.fetchall()
