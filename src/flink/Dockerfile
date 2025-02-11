FROM flink:1.17.2

# Install Python and pip
RUN apt-get update && apt-get install -y python3.11 python3-pip

# Ensure python command points to python3.10
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Install PyFlink
RUN python -m pip install --no-cache-dir apache-flink==1.17.2

# Define JAR versions
ENV FLINK_LIB_DIR="/opt/flink/lib"
ENV JDBC_JAR_VERSION="3.1.2-1.17"
ENV RABBITMQ_JAR_VERSION="3.0.1-1.17"
ENV POSTGRES_JAR_VERSION="42.7.5"

# Download RabbitMQ Connector JAR
RUN curl -fsSL "https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-rabbitmq/${RABBITMQ_JAR_VERSION}/flink-sql-connector-rabbitmq-${RABBITMQ_JAR_VERSION}.jar" \
    -o "${FLINK_LIB_DIR}/flink-sql-connector-rabbitmq-${RABBITMQ_JAR_VERSION}.jar"

# Download PostgreSQL JDBC Connector JAR
RUN curl -fsSL "https://jdbc.postgresql.org/download/postgresql-${POSTGRES_JAR_VERSION}.jar" \
    -o "${FLINK_LIB_DIR}/postgresql-jdbc.jar"

# Download Flink JDBC Connector JAR
RUN curl -fsSL "https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/${JDBC_JAR_VERSION}/flink-connector-jdbc-${JDBC_JAR_VERSION}.jar" \
    -o "${FLINK_LIB_DIR}/flink-connector-jdbc-${JDBC_JAR_VERSION}.jar"

#COPY postgresql-42.7.5.jar /opt/flink/lib/postgresql-42.7.5.jar

WORKDIR /opt/flink