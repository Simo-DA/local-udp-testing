# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory (with producer.py and requirements.txt) to /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the producer script
CMD ["python", "iot_producer.py"]
