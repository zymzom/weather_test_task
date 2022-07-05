from apscheduler.schedulers.asyncio import AsyncIOScheduler
from arq import create_pool
from arq.connections import RedisSettings
from sanic import Sanic, response

from app import settings
from app.db.db_client import PgClient
from app.background.utils import add_scheduler_tasks

app = Sanic(
    'open_weather',
)
app.ctx.db = PgClient()
scheduler = AsyncIOScheduler()


@app.route("/")
async def healthcheck(request):
    """Health check"""
    return response.json("ok")


@app.listener("before_server_start")
async def before_server_start(app, loop):
    """Function that runs before server start."""

    if not await app.ctx.db.check_table_exists():
        await app.ctx.db.create_weather_table()

    redis = await create_pool(RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT))
    add_scheduler_tasks(scheduler=scheduler, redis=redis)
    scheduler.start()

