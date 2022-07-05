from apscheduler.triggers.interval import IntervalTrigger

from app import settings
from app.background.tasks import fetch_current_weather_task


def add_scheduler_tasks(scheduler, redis):
    """Add jobs to fetch weather."""

    for city in settings.CITY_LIST:
        scheduler.add_job(fetch_current_weather_task, IntervalTrigger(seconds=city.frequency), (redis, city))
