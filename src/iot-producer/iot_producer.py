import sys
import pika
import time
from utils.connect_to_rabbitmq import connect_to_rabbitmq
from utils.mock_iot_message import mock_iot_message

# Force stdout to be line-buffered for live-logging inside the container
sys.stdout.reconfigure(line_buffering=True)

print("IoT Producer - Started")
RABBITMQ_QUEUE = "iot-data"
channel = connect_to_rabbitmq()


def publish_message_to_rabbitmq(channel, queue, message):
    try:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange="", routing_key=queue, body=message)
    except pika.exceptions.AMQPConnectionError:
        print("Connection lost. Attempting to reconnect...")
        channel = connect_to_rabbitmq()
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        formatted_time = time.strftime("%d:%m - %H-%M-%S", time.localtime())
        print(f"{formatted_time}: Sent message: queue: {queue}, 'message': {message}")
        time.sleep(10)


# Main function to produce data
def main():
    while True:
        message = mock_iot_message("device-1")
        publish_message_to_rabbitmq(channel, RABBITMQ_QUEUE, message)


if __name__ == "__main__":
    main()
