from kafka import KafkaConsumer
from pymongo import MongoClient
import json,datetime

consumer = KafkaConsumer(
    'sensor_data',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


MONGODB_URI = "mongodb+srv://pswaroop412:manGO43@cluster0.dfdoi6w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URI)
db = client.iot_data
collection = db.sensor_readings

print("Kafka consumer started. Waiting for messages...")

for message in consumer:
    data = message.value
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    collection.insert_one(data)
    print(f"Inserted into MongoDB: {data}")
