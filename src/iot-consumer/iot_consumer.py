import os
import sys
import json
import uuid
from utils.connect_to_rabbitmq import connect_to_rabbitmq
from utils.connect_to_s3 import connect_to_s3
from utils.prepare_consumption import prepare_consumption


# Force stdout to be line-buffered for logging
sys.stdout.reconfigure(line_buffering=True)


QUEUE_NAME = "iot-data"
BUCKET_NAME = "iot-data"
ENDPOINT_URL = "http://s3bucket:9000"

# Establish rabbitMQ connection
print("Iot Consumer - Started")
channel = connect_to_rabbitmq()
# Establish s3 connection
s3_client = connect_to_s3(
    ENDPOINT_URL, os.getenv("MINIO_ACCESS_KEY"), os.getenv("MINIO_SECRET_KEY")
)


def consume_message(channel, method, properties, body):
    try:
        data = json.loads(body.decode())
        print(f"Received message: {data}")

        # create file name s3 bucket
        object_key = f"{data.get('id',uuid.uuid4())}.json"

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=json.dumps(data),
            ContentType="application/json",
        )
        print(f"Uploaded data to S3: {object_key}")

        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Message Acknowledged")
        print(f"-----------")
    except Exception as e:
        print(f"Error while processing message: {e}")


def main(channel):
    channel = prepare_consumption(channel, QUEUE_NAME, consume_message)
    channel.start_consuming()


if __name__ == "__main__":
    main(channel)
