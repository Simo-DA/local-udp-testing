FROM pyflink/playgrounds:1.13.0-rc2

# Download the RabbitMQ connector JAR file
RUN wget -O /opt/flink/lib/rabbitmq.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-rabbitmq_2.12/1.13.0/flink-connector-rabbitmq_2.12-1.13.0.jar

# Download the amqp-client JAR file
RUN wget -O /opt/flink/lib/amqp-client-5.13.0.jar https://repo1.maven.org/maven2/com/rabbitmq/amqp-client/5.13.0/amqp-client-5.13.0.jar

# Set the CLASSPATH environment variable
ENV CLASSPATH /opt/flink/lib/rabbitmq.jar:/opt/flink/lib/amqp-client-5.13.0.jar