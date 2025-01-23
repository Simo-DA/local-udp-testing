# Local UDP Testing

Plattform to localy test components and processes for development of the UDP in a containerized environment.

## Prerequisits

- Docker Desktop

Check if installed and ready

```
docker -v
```

- Docker Compose (Automaticaly installed with latest Docker Desktop Version)

Check if installed and ready

```
docker-compose -v
```

## Getting started

Create .env file to set your Minio secrets. See .env.example:

```
MINIO_ROOT_USER=***YOUR_USERNAME HERE- Min 3 Chars***
MINIO_ROOT_PASSWORD=***YOUR_PASSWORD HERE- Min 8 chars***

MINIO_ACCESS_KEY=***YOUR ACCESS_KEY HERE***
MINIO_SECRET_KEY=***YOUR MINIO_SECRET_KEY HERE***

RABBITMQ_DEFAULT_USER=***YOUR RABBITMQ_DEFAULT_USER HERE - can be anything eg. `guest`***
RABBITMQ_DEFAULT_PASS=***YOUR RABBITMQ_DEFAULT_PASS HERE - can be anything eg. `guest`***
```

# Run Container

1. Make Sure Docker Desktop is up and running
2. Start the container with docker-compose

```
docker compose up -d
```

Use the --build flag if you want rebuild the container without caching.

```
docker compose up -d --build
```

### Ports Services

- Minio UI localhost:9001
- Minio API localhost:9000
- RabbitMQ
