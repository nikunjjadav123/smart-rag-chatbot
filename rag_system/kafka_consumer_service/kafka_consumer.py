from kafka import KafkaConsumer
import json
from vectorstore.index_builder import rebuild_index


consumer = KafkaConsumer(
    "pdf_uploaded",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for msg in consumer:
    event = msg.value

    print(f"🚀 START processing: {event['filename']}")

    rebuild_index()

    print(f"✅ FINISHED processing: {event['filename']}")
    