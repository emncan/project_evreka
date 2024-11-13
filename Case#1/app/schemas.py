from pydantic import BaseModel, condecimal
from datetime import datetime


class LocationDataCreate(BaseModel):
    """
    Pydantic model for creating LocationData entries.
    """

    device_id: str
    latitude: condecimal(ge=-90, le=90)
    longitude: condecimal(ge=-180, le=180)
    speed: float


class LocationDataResponse(BaseModel):
    """
    Pydantic model for serializing LocationData responses.
    """

    id: int
    device_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

    class Config:
        orm_mode = True
