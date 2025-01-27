import json
import boto3
from functools import partial
from datetime import datetime
from dagster import asset, EnvVar

# type hinting
from dagster import ResourceParam
from typing import Callable
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel


BUCKET_NAME = "iot-data"


def consume_message(channel, method, properties, body, s3_client):

    data = json.loads(body.decode())

    timestamp = datetime.fromtimestamp(data["timestamp"])
    year = timestamp.year
    month = f"{timestamp.month:02d}"
    day = f"{timestamp.day:02d}"
    time = f"{timestamp.hour:02d}:{timestamp.minute:02d}:{timestamp.second:02d}"
    object_key = (
        f"{year}/{month}/{day}/device_{data['device_id']}/{time} - {data['id']}.json"
    )

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=json.dumps(data),
        ContentType="application/json",
    )

    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)


@asset(description="Consume data from RabbitMQ´s iot-data queue and store it in S3")
def rabbit_mq_consumer(
    context, rabbitmq_channel: ResourceParam, s3_client: ResourceParam
) -> None:
    queue = "iot-data"
    # create file name s3 bucket
    consume_message_with_s3_lient = partial(consume_message, s3_client=s3_client)
    channel = rabbitmq_channel.get_channel(queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue, on_message_callback=consume_message_with_s3_lient
    )
    channel.start_consuming()
