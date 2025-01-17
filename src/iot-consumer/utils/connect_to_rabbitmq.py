import pika

# Types
from pika.adapters.blocking_connection import BlockingChannel

# docker-compose service name
RABBITMQ_HOST = "rabbitmq"


# Establish connection to RabbitMQ
def connect_to_rabbitmq() -> BlockingChannel:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()
        print("Succesfully connected to RabbitMQ")
    except Exception as e:
        print(f"Error while connection to rabbitmq: {e}")
    return channel
