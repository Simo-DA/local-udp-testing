import paho.mqtt.client as mqtt
import paho.mqtt.enums as enums
import ssl
import boto3
import json
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# MQTT Broker configuration
BROKER_ADDRESS = os.getenv("NIOTIX_BROKER_URI")  # Change to your broker's IP if not on the same machine
PORT = int(os.getenv("NIOTIX_BROKER_PORT"))                   # Default MQTT port
USERNAME = os.getenv("NIOTIX_BROKER_USERNAME")            # Use your configured username
PASSWORD = os.getenv("NIOTIX_BROKER_PASSWORD")            # Use your configured password
TOPIC = os.getenv("NIOTIX_BROKER_TOPIC")

# S3 Configuration
S3_HOST = os.getenv("S3_HOST")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")  
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
logging.info(f"S3_HOST: {S3_HOST}")
logging.info(f"S3_BUCKET_NAME: {S3_BUCKET_NAME}")
logging.info(f"S3_ACCESS_KEY: {S3_ACCESS_KEY}")
logging.info(f"S3_SECRET_KEY: {S3_SECRET_KEY}")

s3_client = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        endpoint_url=S3_HOST
    )

# Create an MQTT client instance
client = mqtt.Client()

# Set the username and password for connection
client.username_pw_set(USERNAME, PASSWORD)


# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        # Subscribe to the topic
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")


# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message from topic '{msg.topic}'")
    try:
        # Parse the payload
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)  # Assuming the payload is JSON

        # Generate a unique file name
        timestamp = datetime.utcnow()
        folder_structure = f"test/{timestamp.year}/{timestamp.month:02}/{timestamp.day:02}"
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


client.tls_set(certfile=None,
               keyfile=None,
               cert_reqs=ssl.CERT_REQUIRED)
# Assign the on_message callback function
client.on_connect = on_connect
client.on_message = on_message


# Connect to the RabbitMQ MQTT broker
try:
    print(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{PORT}...")
    client.connect(BROKER_ADDRESS, PORT, 60)
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit()


# Start the loop to process incoming messages
client.loop_start()
try:
    print(f"Listening for messages on {TOPIC}. Press CTRL+C to exit.")
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    print("Exiting...")

client.loop_stop()
client.disconnect()
