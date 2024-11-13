import asyncio
from app.tasks import process_location_data
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def handle_client(reader, writer):
    """Handles client connection and processes incoming data."""

    addr = writer.get_extra_info('peername')
    logger.info(f"Connection from {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            logger.info(f"Connection closed by {addr}")
            break

        message = data.decode()
        logger.info(f"Received data: {message}")

        if message:
            try:
                device_id, latitude, longitude, speed = message.split(",")
                logger.info(
                    f"Processing data: ID={device_id}, Lat={latitude}, Lon={longitude}, Speed={speed}")

                process_location_data.delay(
                    device_id, float(latitude), float(longitude), float(speed))
                logger.info(f"Worker started for ID={device_id}")
            except ValueError:
                logger.error(
                    f"ValueError: Invalid format in message '{message}'")

    writer.close()
    await writer.wait_closed()


async def start_tcp_server():
    """Starts the TCP server and listens for connections."""

    server = await asyncio.start_server(handle_client, "0.0.0.0", 12345)
    addr = server.sockets[0].getsockname()
    logger.info(f"TCP server started and listening on {addr}...")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_tcp_server())
