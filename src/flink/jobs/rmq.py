from pyflink.datastream import StreamExecutionEnvironment
from pyflink.java_gateway import get_gateway


def main():

    env = StreamExecutionEnvironment.get_execution_environment()

    # Add the RabbitMQ connector JAR files
    env.add_jars(
        "file:///opt/flink/lib/rabbitmq.jar",
        "file:///opt/flink/lib/amqp-client-5.13.0.jar",
    )
    # Use the Java API to create the RabbitMQ source
    gateway = get_gateway()
    RabbitMQSource = (
        gateway.jvm.org.apache.flink.streaming.connectors.rabbitmq.RMQSource
    )
    RMQConnectionConfig = (
        gateway.jvm.org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig
    )

    connection_config = (
        RMQConnectionConfig.Builder()
        .setHost("rabbitmq")
        .setPort(5672)
        .setUserName("{user}")
        .setPassword("{password}")
        .setVirtualHost("/")
        .build()
    )

    rabbitmq_source = RabbitMQSource(
        connection_config,
        "iot-data",
        True,
        gateway.jvm.org.apache.flink.streaming.util.serialization.SimpleStringSchema(),
    )

    # Add the source using the Java API
    stream = env.add_source(rabbitmq_source).add_parallelism(1)

    env.execute("RabbitMQ Source Job")


if __name__ == "__main__":
    main()
