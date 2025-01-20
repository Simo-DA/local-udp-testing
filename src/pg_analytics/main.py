import os
import boto3
import psycopg2


def download_from_s3(bucket_name, access_key, secret_key, file_name, download_path):
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    s3.download_file(bucket_name, file_name, download_path)


def upload_to_postgres(host, dbname, user, password, file_path):
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    cur = conn.cursor()
    with open(file_path, "r") as f:
        cur.copy_expert("COPY your_table FROM STDIN WITH CSV HEADER", f)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    bucket_name = os.getenv("S3_BUCKET")
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    file_name = "data.csv"
    download_path = "/tmp/data.csv"

    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_db = os.getenv("POSTGRES_DB")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")

    download_from_s3(bucket_name, access_key, secret_key, file_name, download_path)
    upload_to_postgres(
        postgres_host, postgres_db, postgres_user, postgres_password, download_path
    )
