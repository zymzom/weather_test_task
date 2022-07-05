import asyncpg

from app import settings
from app.db.queries import CREATE_WEATHER_TABLE, EXIST_WEATHER_TABLE


class PgClient:
    """Postgres client class."""

    @staticmethod
    async def create_pool() -> asyncpg.pool.Pool:
        """Return created asyncpg pool"""

        return await asyncpg.create_pool(
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

    async def fetch(self, sql, *args, **kwargs):
        pool = await self.create_pool()
        async with pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)

    async def fetch_row(self, sql, *args, **kwargs):
        pool = await self.create_pool()
        async with pool.acquire() as connection:
            return await connection.fetchrow(sql, *args, **kwargs)

    async def execute(self, sql, *args, **kwargs):
        pool = await self.create_pool()
        async with pool.acquire() as connection:
            return await connection.execute(sql, *args, **kwargs)

    async def fetch_val(self, sql, *args, **kwargs):
        pool = await self.create_pool()
        async with pool.acquire() as connection:
            return await connection.fetchval(sql, *args, **kwargs)

    async def check_table_exists(self) -> bool:
        """Check for open weather table."""
        result = await self.fetch_val(EXIST_WEATHER_TABLE, 'open_weathers')
        return result

    async def create_weather_table(self):
        """Create open weather table."""

        pool = await self.create_pool()
        async with pool.acquire() as connection:
            await connection.execute(CREATE_WEATHER_TABLE)
        await pool.close()
