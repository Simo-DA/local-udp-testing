import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.rabbitmq import RMQSource, RMQConnectionConfig

RABBITMQ_QUEUE = "iot-data"
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")

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
    queue_name=RABBITMQ_QUEUE,  # Replace with your RabbitMQ queue name
    use_correlation_id=True,
    deserialization_schema=SimpleStringSchema(),
)

# Add Source to Stream
stream = env.add_source(rmq_source)


# Convert raw stream into a format suitable for PostgreSQL
# Assume messages are simple strings (e.g., sensor readings)
# formatted_stream = stream.map(lambda msg: (msg,), output_type=Types.TUPLE([Types.STRING()]))

# Define PostgreSQL Sink
# jdbc_sink = JdbcSink.sink(
#     "INSERT INTO iot_messages (message) VALUES (?)",
#     Types.ROW([Types.STRING()]),  # Map data to SQL
#     JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
#         .with_url("jdbc:postgresql://postgres-db:5432/mydatabase")  # Update DB name if needed
#         .with_driver_name("org.postgresql.Driver")
#         .with_user_name("postgres")
#         .with_password("postgres")
#         .build(),
#     JdbcExecutionOptions.builder()
#         .with_batch_interval_ms(1000)
#         .with_batch_size(5)
#         .with_max_retries(3)
#         .build()
# )

# # Add Sink to Stream
# formatted_stream.add_sink(jdbc_sink)

# Process the stream (print for now)
stream.print()

# Execute the PyFlink job
env.execute("RabbitMQ to PostgreSQL Streaming Job")
