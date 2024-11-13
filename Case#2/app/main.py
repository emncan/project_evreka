from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, Base, engine
from .models import LocationData
from typing import List
from .schemas import LocationDataResponse
from sqlalchemy.future import select
from datetime import datetime

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Creates database tables on startup."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/api/location/{device_id}/latest/",
         response_model=LocationDataResponse)
async def get_latest_location(
        device_id: str,
        db: AsyncSession = Depends(get_db)):
    """Fetches the latest location data for a device."""

    result = await db.execute(
        select(LocationData)
        .where(LocationData.device_id == device_id)
        .order_by(LocationData.timestamp.desc())
        .limit(1)
    )
    location = result.scalar_one_or_none()

    if location is None:
        raise HTTPException(status_code=404, detail="Location data not found")

    return location


@app.get("/api/location/{device_id}/",
         response_model=List[LocationDataResponse])
async def get_location_data(
        device_id: str,
        start_date: datetime,
        end_date: datetime,
        db: AsyncSession = Depends(get_db)):
    """Fetches location data for a device within a date range."""

    result = await db.execute(
        select(LocationData)
        .where(LocationData.device_id == device_id)
        .where(LocationData.timestamp.between(start_date, end_date))
        .order_by(LocationData.timestamp.desc())
    )
    locations = result.scalars().all()

    if not locations:
        raise HTTPException(
            status_code=404,
            detail="Location data not found within the specified date range")

    return locations
