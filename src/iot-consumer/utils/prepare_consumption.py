# Types
from typing import Callable
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


def prepare_consumption(
    channel: BlockingChannel,
    queue_name: str,
    callback_function: Callable[[Basic.Deliver, BasicProperties, bytes], None],
) -> BlockingChannel:
    try:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=callback_function)
        channel.queue_declare(queue=queue_name, durable=True)
        print(f"Consumption for {queue_name} prepared")
        return channel
    except Exception as e:
        print(f"Error while preparing consumption: {e}")
