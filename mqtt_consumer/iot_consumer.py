import paho.mqtt.client as mqtt
import paho.mqtt.enums as enums

import ssl
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# MQTT Broker configuration
BROKER_ADDRESS = os.getenv("NIOTIX_BROKER_URI")  # Change to your broker's IP if not on the same machine
PORT = int(os.getenv("NIOTIX_BROKER_PORT"))                   # Default MQTT port
USERNAME = os.getenv("NIOTIX_BROKER_USERNAME")            # Use your configured username
PASSWORD = os.getenv("NIOTIX_BROKER_PASSWORD")            # Use your configured password
TOPIC = os.getenv("NIOTIX_BROKER_TOPIC")

# Create an MQTT client instance
client = mqtt.Client() #mqtt.Client(callback_api_version=enums.CallbackAPIVersion.VERSION2)

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
def on_message(client, userdata, message):
    print(f"Received message from topic '{message.topic}': {message.payload.decode()}")


client.tls_set(certfile=None,
               keyfile=None,
               cert_reqs=ssl.CERT_REQUIRED)
# Assign the on_message callback function
client.on_connect = on_connect
client.on_message = on_message


# Connect to the RabbitMQ MQTT broker
try:
    client.connect(BROKER_ADDRESS, PORT, 60)
    print(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{PORT}...")
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
