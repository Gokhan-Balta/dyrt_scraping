import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.scraper.dyrt_scraper import fetch_and_save
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

async def start_scheduler():
    trigger = CronTrigger(hour=3, minute=0)
    scheduler.add_job(fetch_and_save, trigger)
    print("The timer has been started. It will run every day at 03:00.")
    scheduler.start()
