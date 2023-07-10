import os
import time
import json
from kafka import KafkaProducer


# Setup configurations
data_dir = "path_to_log_files"  # log files directories
kafka_broker = "kafka-ip-address:port"  # broker
kafka_topic = "producer-topic"  # topic

# create producer to send data through it

producer = KafkaProducer(bootstrap_servers=kafka_broker)

def process_file(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            # Create a message to be sent to Kafka
            message = {
                'log_line': line.strip()  # Remove any trailing newline characters
            }

            # Serialize the message to JSON
            message_json = json.dumps(message).encode('utf-8')

            # Send the message to Kafka
            producer.send(kafka_topic, message_json)

        # Close the producer
        producer.flush()

# Get the log files
processed_files = set()

while True:
    # List all log files
    files = [f for f in os.listdir(data_dir) if f.endswith('.log')]

    # Process any new files
    for file in files:
        if file not in processed_files:
            process_file(data_dir + file)
            processed_files.add(file)
    

    # Wait for a while before checking the directory again
    time.sleep(2)