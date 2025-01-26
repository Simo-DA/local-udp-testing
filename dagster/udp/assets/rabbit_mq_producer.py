import pika
import json
import uuid
import time
import random
from dagster import asset, EnvVar

# type hinting
from typing import Union
from dagster import ResourceParam


def mock_iot_message(device_id: str) -> dict[str, Union[str, float, int]]:
    id = str(uuid.uuid4())
    temperature = 10.0 + random.uniform(-15.0, 15.0)
    timestamp = time.time()
    message = {
        "device_id": device_id,
        "id": id,
        "temperature": temperature,
        "timestamp": timestamp,
    }

    return message


@asset
def rabbit_mq_producer(context, rabbitmq_channel: ResourceParam) -> None:
    queue: str = "iot-data"
    message: dict = mock_iot_message(1)
    
    channel = rabbitmq_channel.get_channel(queue)
    context.log.info(f"Connected to RabbitMQ")
    channel.basic_publish(exchange="", routing_key=queue, body=json.dumps(message))
    context.log.info(f"Published message: {message}")
    
