import os
import pika
import json
import uuid
import boto3
from dagster import asset, EnvVar

# type hinting
from dagster import ResourceParam
from typing import Callable
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel


BUCKET_NAME = "iot-data"
ENDPOINT_URL = "http://s3bucket:9000"


def connect_to_s3(
    endpoint_url: str, access_key_id: str, secret_access_key: str
) -> boto3.client:
    access_key_id = EnvVar("MINIO_ACCESS_KEY").get_value()
    secret_access_key = EnvVar("MINIO_SECRET_KEY").get_value()
    
    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    return s3_client


def prepare_consumption(
    channel: BlockingChannel,
    queue_name: str,
    callback_function: Callable[[Basic.Deliver, BasicProperties, bytes], None],
) -> BlockingChannel:

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback_function)

    return channel


def consume_message(channel, method, properties, body):

    data = json.loads(body.decode())
    object_key = f"{uuid.uuid4()}.json"
    # create file name s3 bucket
    s3_client = connect_to_s3(
        ENDPOINT_URL, os.getenv("MINIO_ACCESS_KEY"), os.getenv("MINIO_SECRET_KEY")
    )

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=json.dumps(data),
        ContentType="application/json",
    )

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)


@asset
def rabbit_mq_consumer(context, rabbitmq_channel: ResourceParam) -> None:
    queue = "iot-data"

    channel = rabbitmq_channel.get_channel(queue)
    channel = prepare_consumption(channel, queue, consume_message)
    channel.start_consuming()
