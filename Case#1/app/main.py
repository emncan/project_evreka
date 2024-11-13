from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine
from .models import Base
from .crud import get_latest_data, get_data_by_date_range
from .schemas import LocationDataCreate, LocationDataResponse
from .tasks import save_location_data
from typing import List
from datetime import datetime

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """
    Creates the database tables on startup.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/api/location/")
async def create_data(
        location_data: LocationDataCreate,
        db: AsyncSession = Depends(get_db)):
    """
    Accepts location data and processes it asynchronously.
    """

    try:
        save_location_data.delay(location_data.dict())
        return {"status": "Data is being processed"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing data: {e}")


@app.get("/api/location/{device_id}/latest/",
         response_model=LocationDataResponse)
async def get_latest(device_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the latest location data for a device.
    """

    data = await get_latest_data(db, device_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Location data not found")
    return data


@app.get("/api/location/{device_id}/",
         response_model=List[LocationDataResponse])
async def get_data_by_range(
        device_id: str,
        start_date: datetime,
        end_date: datetime,
        db: AsyncSession = Depends(get_db)):
    """
    Retrieves location data for a device within a specified date range.
    """

    data = await get_data_by_date_range(db, device_id, start_date, end_date)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Location data not found within the specified date range")
    return data
