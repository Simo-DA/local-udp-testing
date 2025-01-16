import pika
import json
import time
import random
import uuid
from typing import Union


RABBITMQ_HOST = "rabbitmq"
RABBITMQ_QUEUE = "iot-data"


# Establish connection to RabbitMQ
def connect_to_rabbitmq() -> (
    Union[pika.adapters.blocking_connection.BlockingChannel, None]
):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        print("Successfully connected to RabbitMQ")
        return connection.channel()
    except Exception as e:
        print("Error connecting to RabbitMQ: ", e)
        return None


def create_iot_message(device_id: str) -> dict[str, Union[str, float, int]]:
    id = str(uuid.uuid4())
    temperature = 10.0 + random.uniform(-15.0, 15.0)
    timestamp = time.time()
    message = json.dumps(
        {
            "device_id": device_id,
            "id": id,
            "temperature": temperature,
            "timestamp": timestamp,
        }
    )
    return message


# Send a message to RabbitMQ
def publish_message(
    channel: pika.adapters.blocking_connection.BlockingChannel, queue: str, message: str
) -> None:
    try:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange="", routing_key=queue, body=message)
        print(f"Sent message: {message}")
    except Exception as e:
        print("Error sending message: ", e)


# Main function to produce data
def main():
    print("Starting IoT Producer")
    while True:
        channel = connect_to_rabbitmq()
        try:
            message = create_iot_message("device-1")
            print(message)
            publish_message(channel, RABBITMQ_QUEUE, message)
            time.sleep(5)  # Simulate time delay between messages
        except Exception as e:
            print("Error in main loop: ", e)
        channel.close()


if __name__ == "__main__":
    main()
