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
6. Flink (Real Time Transformations)
   1. Flink Jobmanager
   2. Flink Taskmanager

### Unconnected services

- Great Expecations
- Airbyte
- PG Analytics

### Open **questions**

- How to deploy rabbit mq consumer? Currently continuous materialization in dagster. Good solution?
- How to create postgres sink in flink job?
- Compatability of RabbitMQ-Connector (v1.17) with latest flink version (1.20)
- How to connect s3_bucket with postgresdb?

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
- PostgresDB [localhost:5432](http://localhost:5432)
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

Both Flink services (Taskmanager and Jobmanager) are built with the same [Dockerfile](src\flink\Dockerfile).

#### Flink Jobmanager

Responsible to start and manage Flink Jobs. There is usually only one Jobmanager and you can have several Taskmanagers to run the jobs.

#### Flink Taskmanager

Is actually running the task. Worker node? --> further research necessary

#### Job Submission

The Job submission is automated with the [start.sh](src\flink\jobmanager\start.sh) which is mounted to the container and defined as entrypoint for the Jobmanager service in [Docker-Compose]("docker-compose.yml"). Thereby all files inside the flink/jobs/ folder are automaticaly ran, when the container is started.

-> Errors in Scripts will kill the whole Jobmanager service!!!

##### Manually submitting Jobs

To manually submit a job run the following command inside the containers terminal:

```
flink run -m flink-jobmanager:8081 -py /path/to/your/job/in/container/example_job.py
```

<hr style="height:1px;">

### Dagster

Access the [Dagster UI here](http://localhost:3000). Use Dagster to orchestrate your data pipelines.

#### Assets

Smalles building blocks of Dagster Jobs. Naming should be

#### Jobs

Tasks that can be ran by automated with schedules. Can consist of one or many assets.

#### Ressources

Reusable connections configurations for common services (postgres, s3, rabbitmq).

#### Schedules

Plans (eg. cron jobst) to automaticly run Dagster Jobs.

#### Definitions.py

[Definitions.py](src\dagster\udp\definitions.py) is used to collect all building blocks (assets, jobs, ressources and schedules) for one Code Space. They are only accesible for docker if they are collected here.

Different Code Spaces are used if dependencies of projects differ grately or should rather by managed seperatly.

#### Bind Mount

#### Project Structure

<hr style="height:1px;">
