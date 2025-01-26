import boto3
from dagster import ressource, EnvVar



@ressource
def s3_client() -> boto3.client:
    endpoint_url = "http://s3bucket:9000"
    access_key_id = EnvVar("MINIO_ACCESS_KEY").get_value()
    secret_access_key = EnvVar("MINIO_SECRET_KEY").get_value()
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
