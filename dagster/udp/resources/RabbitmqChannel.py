import pika
from dagster import EnvVar, ConfigurableResource

# Types
from pika.adapters.blocking_connection import BlockingChannel


class RabbitmqChannel(ConfigurableResource):

    def get_channel(self, queue) -> BlockingChannel:
        rabbitmq_host = EnvVar("RABBITMQ_HOST").get_value()
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        return channel
