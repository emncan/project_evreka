from celery import Celery
import asyncio
from .database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .models import LocationData
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

celery = Celery("tasks", broker="pyamqp://rabbitmq//")


@celery.task
def process_location_data(device_id, latitude, longitude, speed):
    """Processes and saves location data asynchronously."""

    logger.info(f"Starting Celery loop...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_task(device_id, latitude, longitude, speed))


async def run_task(device_id, latitude, longitude, speed):
    """Runs the task to save location data."""

    logger.info(f"Run Task...")
    async with async_session() as db:
        await save_location_data(db, device_id, latitude, longitude, speed)


async def save_location_data(db, device_id, latitude, longitude, speed):
    """Saves location data to the database."""

    location_data = LocationData(
        device_id=device_id,
        latitude=latitude,
        longitude=longitude,
        speed=speed
    )
    logger.info(f"Creating new LocationData: {location_data}")
    db.add(location_data)
    await db.commit()
    await db.refresh(location_data)
