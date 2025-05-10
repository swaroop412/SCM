from kafka import KafkaConsumer
from pymongo import MongoClient, errors
import json
import time
import datetime
import sys

KAFKA_TOPIC = 'sensor_data'
KAFKA_BROKER = 'kafka:9092'
MONGO_URI = "mongodb+srv://pswaroop412:manGO43@cluster0.dfdoi6w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Retry Kafka connection
for attempt in range(10):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='sensor-consumer-group'
        )
        print("[✓] Connected to Kafka.")
        break
    except Exception as e:
        print(f"[!] Kafka connection failed: {e}. Retrying ({attempt + 1}/10)...")
        time.sleep(5)
else:
    print("[✗] Kafka is not available after multiple attempts. Exiting.")
    sys.exit(1)

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client.iot_data
    collection = db.sensor_readings
    print("[✓] Connected to MongoDB.")
except errors.ConnectionFailure as e:
    print(f"[✗] MongoDB connection error: {e}")
    sys.exit(1)

print("[*] Kafka consumer started. Waiting for messages...")

for message in consumer:
    try:
        data = message.value
        data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        collection.insert_one(data)
        print(f"[→] Inserted into MongoDB: {data}")
    except Exception as e:
        print(f"[!] Error inserting data: {e}")
