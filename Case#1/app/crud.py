from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from .models import LocationData
from .schemas import LocationDataCreate
from datetime import datetime
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def create_location_data(
        db: AsyncSession,
        location_data: LocationDataCreate):
    """
    Creates a new LocationData entry in the database.
    """

    try:
        db_data = LocationData(**location_data.dict())
        logger.debug(f"Creating new LocationData: {db_data}")
        db.add(db_data)
        await db.commit()
        await db.refresh(db_data)
        return db_data
    except SQLAlchemyError as e:
        await db.rollback()  # Rollback in case of error
        logger.error(f"Error while creating LocationData: {e}")
        raise


async def get_latest_data(db: AsyncSession, device_id: str):
    """
    Retrieves the latest LocationData for a given device_id.
    """

    result = await db.execute(
        select(LocationData)
        .where(LocationData.device_id == device_id)
        .order_by(LocationData.timestamp.desc())
    )
    return result.scalars().first()


async def get_data_by_date_range(
        db: AsyncSession,
        device_id: str,
        start_date: datetime,
        end_date: datetime):
    """
    Retrieves LocationData for a given device_id within the specified date range.
    """

    result = await db.execute(
        select(LocationData)
        .where(LocationData.device_id == device_id)
        .where(LocationData.timestamp.between(start_date, end_date))
        .order_by(LocationData.timestamp.desc())
    )
    return result.scalars().all()
