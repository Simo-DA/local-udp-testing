import boto3
from dagster import resource, EnvVar


@resource
def s3_client() -> boto3.client:
    return boto3.client(
        "s3",
        endpoint_url=EnvVar("MINIO_ENDPOINT").get_value(),
        aws_access_key_id=EnvVar("MINIO_ACCESS_KEY").get_value(),
        aws_secret_access_key=EnvVar("MINIO_SECRET_KEY").get_value(),
    )
