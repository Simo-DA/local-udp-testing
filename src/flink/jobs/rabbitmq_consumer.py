import os
import json
from datetime import datetime

from pyflink.table import Row
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.rabbitmq import RMQSource, RMQConnectionConfig
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions, JdbcExecutionOptions


RABBITMQ_QUEUE = "iot-data"
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")

# Initialize StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# RabbitMQ Connection Configuration
rmq_connection = (
    RMQConnectionConfig.Builder()
    .set_host(RABBITMQ_HOST)
    .set_port(RABBITMQ_PORT)
    .set_virtual_host("/")
    .set_user_name(RABBITMQ_USER)
    .set_password(RABBITMQ_PASS)
    .build()
)

# Define RabbitMQ Source
rmq_source = RMQSource(
    connection_config=rmq_connection,
    queue_name=RABBITMQ_QUEUE,
    use_correlation_id=True,
    deserialization_schema=SimpleStringSchema(),
)

#Define PostgreSQL Sink
jdbc_sink = JdbcSink.sink(
    "INSERT INTO iot_messages (message) VALUES (?)",
    Types.ROW([Types.STRING(),]),  # Map data to SQL
    JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
        .with_url(f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/mydatabase")  # Update DB name if needed
        .with_driver_name("org.postgresql.Driver")
        .with_user_name(POSTGRES_USER)
        .with_password(POSTGRES_PASS)
        .build(),
    JdbcExecutionOptions.builder()
        .with_batch_interval_ms(1000)
        .with_batch_size(5)
        .with_max_retries(3)
        .build()
)

# 1. Add Source to Stream
stream = env.add_source(rmq_source)

stream.print()

# 2. Convert raw stream into a format suitable for PostgreSQL
# Assume messages are simple strings (e.g., sensor readings)
formatted_stream = stream.map(lambda msg: Row(json.dumps(msg)), output_type=Types.ROW([Types.STRING()]))

formatted_stream.print()

# 3. Add Sink to Stream
formatted_stream.add_sink(jdbc_sink)

# 4. Execute the PyFlink job
env.execute("RabbitMQ to PostgreSQL Streaming Job")
