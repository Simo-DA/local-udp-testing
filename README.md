# Local UDP Testing

Plattform to localy test components and processes for development of the UDP in a containerized environment.

## Prerequisits

- Docker Desktop

Check if installed and ready

```
docker-compose -v
```

- Docker Compose (Automaticaly installed with latest Docker Desktop Version)

Check if installed and ready

```
docker-compose -v
```

## Getting started

Create .env file to set your Minio secrets. See .env.example:

```
MINIO_ROOT_USER=***YOUR_USERNAME - Min 3 Chars***
MINIO_ROOT_PASSWORD=***YOUR_PASSWORD - Min 8 chars***
```

# Run Container

1. Make Sure Docker Desktop is up and running
2. Start the container with docker-compose

```
docker compose up -d
```

### Ports Services

- Minio UI localhost:9001
- Minio API localhost:9000
