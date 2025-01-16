import os
import pika
import boto3
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "iot-data"

s3_client = boto3.client(
    "s3",
    endpoint_url="http://s3bucket:9000",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)
BUCKET_NAME = "iot-data"
try:
    print(s3_client.list_objects_v2(Bucket=BUCKET_NAME))
except Exception as e:
    print("Error to print bucket: ", e)


def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

    data = json.loads(body.decode())
    object_key = f"{data.get('id',uuid.uuid4())}.json"
    # Upload data to S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=json.dumps(data),
        ContentType="application/json",
    )
    print(f"Uploaded data to S3: {object_key}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    return channel


def main():

    channel = connect_to_rabbitmq()
    print(f"Waiting for messages in {QUEUE_NAME}...")
    channel.start_consuming()


if __name__ == "__main__":

    main()
