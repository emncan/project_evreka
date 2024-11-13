# FastAPI Location Data Service

This is a FastAPI-based application for processing and retrieving location data. It supports asynchronous database operations using SQLAlchemy, data processing via Celery with RabbitMQ, and communication via a TCP server. The project is containerized using Docker.

## Features

- **FastAPI** for the web API.
- **Celery** for background tasks.
- **PostgreSQL** for data storage.
- **RabbitMQ** for task queuing.
- **TCP Server** for receiving location data from external devices.

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

- **FastAPI**: The main API application running on port `8000`.
- **PostgreSQL**: The database service, which will run on port `5438`.
- **RabbitMQ**: The task queue service, accessible at port `5672`.
- **Celery**: The worker that processes background tasks.
- **TCP Server**: Listens on port 12345 for incoming data.

#### Step 2: Access the API
Once the containers are up and running, the FastAPI application will be available at:
```bash
http://localhost:8000
```
You can access the automatic API documentation at:
- **Swagger UI**: http://localhost:8000/docs#/
- **ReDoc UI**: http://localhost:8000/redoc

![image](https://github.com/user-attachments/assets/7e550b40-403b-4a8a-9108-b4919061cc2e)

### 2. API Usage

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

### 3. Sending Location Data (TCP Server)
The TCP server listens for incoming data on port 12345. Each message should contain the following comma-separated values:

```bash
device_id,latitude,longitude,speed
```

The following sample python script can be used to send data to the TCP server.

```bash
import socket
import random
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

try:
    for _ in range(10):
        device_id = f"device{random.randint(100, 999)}"
        latitude = round(random.uniform(39.0, 41.0), 6)  
        longitude = round(random.uniform(32.0, 34.0), 6)  
        speed = round(random.uniform(0.0, 120.0), 2)     

        data = f"{device_id},{latitude},{longitude},{speed}"
        
        client_socket.sendall(data.encode())
        time.sleep(1)

finally:
    client_socket.close()

```

The TCP server will forward this data to the Celery worker for processing and storage.

### 4. Stop the Docker Containers
To stop the containers, use the following command:
```bash
docker-compose down
```