# Local UDP Testing

Plattform to localy test components and processes for development of the UDP in a containerized environment.

## Current State

![alt text](overview.excalidraw.png)

### Connected Services

1. How to persist config without other meta data? (S3 + rabbitmq)
2. rabbitmq Message Broker ( currently one queue: "iot-data")
3. s3bucket (MinIO)
   1. "iot-data" - bucket
   2. AccesKey and Secret manualy created (persisted with mount in s3bucket folder)
4. postgres-db
   1. postgres database (unused)
   2. dagster database (used by dagster)
5. Dagster as Data Pipeline Orchestrator
   1. iot-produce job (scheduled every minute)
      1. rabbit-mq-producer asset
   2. rabbitMQ-consumer asset manualy materialized. Runs continuosly (iot-data queue -> iot-data bucket)
   3. Ressources
      1. RabbitMQ_channel
      2. s3_client

### Unconnected services

- Flink (Real Time Analytics) -> skeleton already in docker-compose
  - Task Manager
  - Job-Manager
- Great Expecations

### Open **questions**

- How to deploy rabbit mq consumer? Currently continuous materialization in dagster. Good solution?
- How to connect RabbitMQ iot-data queue to flink?
- How to connect s3_bucket with postgresdb?
- How to connect flink with postgres?

## Prerequisits

- Docker Desktop

Check if installed and ready

```bash
docker -v
```

- Docker Compose (Automaticaly installed with latest Docker Desktop Version)

Check if installed and ready

```bash
docker-compose -v
```

## Getting started

Necessary Secrets are already created in the [.env](./.env). So you only need to run the container.


## Run Container

1. Make Sure Docker Desktop is up and running
2. Start the container with docker-compose

```bash
docker compose up -d
```

Use the --build flag if you want rebuild the container without caching.

```bash
docker compose up -d --build
```

## Usage and Services

### Port Mapping

- MinIO UI [localhost:9001](http://localhost:9001)
- MinIO API [localhost:9000](http://localhost:9000)
- PostgresDB [localhost:5433](http://localhost:5433)
- RabbitMQ messaging [localhost:5672](http://localhost:5672)
- RabbitMQ management UI [localhost:15672](http://localhost:15672)
- Flink UI [localhost:8081](http://localhost:8081)
- Dagster UI [localhost:3000](http://localhost:3000)

<hr style="height:1px;">

### MinIO

MinIO is used to create a local S3-Bucket service. Got to the [MinIO-UI](http://localhost:9001) and login with the credentials (MINIO_ROOT_USER, MINIO_ROOT_PASSWORD) set in your [.env](./.env) file.

#### Usage

You can manualy add new buckets or create access keys, users and user-roles.

#### Bind-Mount

The containers data folder is connected to the local [src/s3bucket/data](src/s3bucket/data)-folder. That way buckets, bucket-data and credentials can be persisited between builds and shared inside the repository.

<hr style="height:1px;">

### RabbitMQ

Acces the [RabbitMQ-UI here](http://localhost:15672) and login with the creadentials set for RABBITMQ_USER and RABBITMQ_PASS in your [.env](./.env) file. The default value is guest for both user and pass.

<hr style="height:1px;">

### PostgresDB

Use Database-Management-Tool (eg. PGAdmin) to connect to the Databese. Use connection settings set in your [.env](./.env) file.

<hr style="height:1px;">

### Flink UI

Acces the [Flink-UI here](http://localhost:8081).

To submit a job, type inside a terminal of the container: flink run -m flink-jobmanager:8081 -py /opt/flink/jobs/rabbitmq_consumer.py

<hr style="height:1px;">

### Dagster

Access the [Dagster UI here](http://localhost:3000). Use Dagster to orchestrate your data pipelines.

#### Bind Mount

#### Project Structure

<hr style="height:1px;">
