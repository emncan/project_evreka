from pydantic import BaseModel
from datetime import datetime


class LocationDataResponse(BaseModel):
    """Schema for location data response."""

    device_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

    class Config:
        orm_mode = True
