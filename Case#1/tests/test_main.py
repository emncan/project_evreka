import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import LocationDataCreate, LocationDataResponse
from datetime import datetime, timedelta

client = TestClient(app)


def test_create_data():
    location_data = {
        "device_id": "test_device_1",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 50.0
    }

    response = client.post("/api/location/", json=location_data)

    assert response.status_code == 200
    assert response.json() == {"status": "Data is being processed"}


def test_get_latest_data():
    device_id = "test_device_1"
    mock_data = LocationDataResponse(
        id=1,
        device_id=device_id,
        latitude=40.7128,
        longitude=-74.0060,
        speed=50.0,
        timestamp=datetime.utcnow()
    )

    mock_data_dict = mock_data.dict()
    mock_data_dict["timestamp"] = mock_data.timestamp.isoformat()

    with client:
        response = client.get(f"/api/location/{device_id}/latest/")

    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == mock_data.device_id
    assert data["latitude"] == mock_data.latitude
    assert data["longitude"] == mock_data.longitude
    assert data["speed"] == mock_data.speed
    assert "timestamp" in data


def test_get_data_by_range():
    device_id = "test_device_1"
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(minutes=5)

    mock_data = [
        LocationDataResponse(
            id=1,
            device_id=device_id,
            latitude=40.7128,
            longitude=-74.0060,
            speed=50.0,
            timestamp=datetime.utcnow()
        ),
        LocationDataResponse(
            id=2,
            device_id=device_id,
            latitude=40.7138,
            longitude=-74.0070,
            speed=60.0,
            timestamp=datetime.utcnow() + timedelta(minutes=1)
        ),
    ]

    mock_data_list = [data.model_dump() for data in mock_data]
    for item in mock_data_list:
        item["timestamp"] = item["timestamp"].isoformat()

    with client:
        response = client.get(
            f"/api/location/{device_id}/?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Location data not found within the specified date range"}
