from celery import Celery
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session
from .crud import create_location_data
from .schemas import LocationDataCreate

celery = Celery("tasks", broker="pyamqp://rabbitmq//")


@celery.task
def save_location_data(location_data: dict):
    """
    Celery task to process and save location data asynchronously.
    """

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_task(location_data))


async def run_task(location_data: dict):
    """
    Handles the creation of LocationData in the database asynchronously.
    """

    async with async_session() as db:
        await create_location_data(db, LocationDataCreate(**location_data))
