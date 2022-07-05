from app.models.cities import City


async def fetch_current_weather_task(redis, city: City):
    """Fetch weather for chosen city."""
    await redis.enqueue_job('weather_task', city)
