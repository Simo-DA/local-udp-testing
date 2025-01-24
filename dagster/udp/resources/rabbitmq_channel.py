import os
import pika
from dagster import resource, EnvVar

# Types
from pika.adapters.blocking_connection import BlockingChannel


@resource
def rabbitmq_channel_resource() -> BlockingChannel:
    rabbitmq_host = EnvVar("RABBITMQ_HOST")
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    return connection.channel()
