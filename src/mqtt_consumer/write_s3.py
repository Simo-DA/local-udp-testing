import boto3
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# AWS S3 Configuration
S3_HOST = os.getenv("S3_HOST")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")  
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
print(S3_HOST)
print(S3_BUCKET_NAME)
print(S3_ACCESS_KEY)
print(S3_SECRET_KEY)

s3_client = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        endpoint_url=S3_HOST
    )

class MockMessage:
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload

def write_msg_to_s3(msg):
    try:
        # Parse the payload
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)  # Assuming the payload is JSON

        # Generate a unique file name
        timestamp = datetime.utcnow()
        folder_structure = f"{msg.topic.replace('/', '_')}/{timestamp.year}/{timestamp.month:02}/{timestamp.day:02}"
        file_name = f"{folder_structure}/message_{timestamp.strftime('%H%M%S')}.json"
        #file_name = f"{msg.topic.replace('/', '_')}_{timestamp}.json"

        #response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Delimiter='/')

        # Upload the file to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(data),
            ContentType="application/json",
        )
        print(f"Message written to S3 bucket {S3_BUCKET_NAME} as {file_name}")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Create a mock MQTT message
    mock_msg = MockMessage(
        topic="test/topic",
        payload=json.dumps({"key": "value", "temperature": 22.5}).encode("utf-8")
    )

    # Test writing to S3
    write_msg_to_s3(mock_msg)

if __name__ == "__main__":
    main()
