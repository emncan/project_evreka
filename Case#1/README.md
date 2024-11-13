# Location Data FastAPI Project

This project is a FastAPI-based application that processes location data asynchronously using Celery and stores it in a PostgreSQL database. It also provides endpoints to retrieve location data for specific devices within a given date range.

## Features

- Asynchronous location data creation and storage using Celery and RabbitMQ.
- Retrieve the latest location data for a specific device.
- Fetch location data within a specified date range.
- PostgreSQL database for data storage.

## Requirements

- Python 3.9+
- Docker (for easy setup of services like PostgreSQL and RabbitMQ)

## Setup Instructions

### 1. Build and Run with Docker

This project uses Docker to set up the necessary services.
#### Step 1: Build and start the containers
In the project root directory, run the following command to build and start the Docker containers:

```bash
docker-compose up --build
```
This will start the following services:

- **db**: PostgreSQL database
- **rabbitmq**: RabbitMQ message broker (used by Celery)
- **web**: FastAPI web server
- **worker**: Celery worker to process background tasks

#### Step 2: Access the API
Once the containers are up and running, the FastAPI application will be available at:
```bash
http://localhost:8000
```
You can access the automatic API documentation at:
- **Swagger UI**: http://localhost:8000/docs#/
- **ReDoc UI**: http://localhost:8000/redoc

![image](https://github.com/user-attachments/assets/ba733202-0485-4424-840a-ccfd1004d72f)


### 2. Usage

#### Create Location Data
To create location data for a device, send a POST request to `/api/location/` with the following JSON payload:

```bash
POST: GET: http://localhost:8000/api/location/
{
  "device_id": "device123",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "speed": 55.5
}
```
The data will be processed asynchronously and stored in the PostgreSQL database.

#### Retrieve Latest Location Data
To retrieve the latest location data for a device, send a GET request to `/api/location/{device_id}/latest/`.

```bash
GET: http://localhost:8000/api/location/device123/latest/
```

#### Retrieve Location Data by Date Range
To retrieve location data for a device within a specific date range, send a GET request to`/api/location/{device_id}/`.

Include the `start_date` and `end_date` as query parameters in the request.

```bash
GET: http://localhost:8000/api/location/device123/?start_date=2024-11-13T13%3A46%3A56&end_date=2024-11-13T13%3A50%3A56
```
### 3. Running Tests with pytest Inside Docker
To run tests inside your Docker container using pytest, follow these steps:

#### 1. Access the Running Docker Container
Once the containers are running, you can access the web service container using the docker exec command.

First, find the name or ID of the running web container:
```bash
docker ps
```
This will show the list of running containers. Look for the container running the web service (your FastAPI app), and note the container name or ID

Then, use the following command to access the container’s shell:

```bash
docker exec -it <container_name> sh
```
Replace <container_name> with the actual name or ID of your container.

#### 2. Run the Tests
Once inside the container, you can run pytest to execute your tests:
```bash
pytest -k test_create_data
pytest -k test_get_latest_data
pytest -k test_get_data_by_range
```

### 4. Stop the Docker Containers
To stop the containers, use the following command:
```bash
docker-compose down
```