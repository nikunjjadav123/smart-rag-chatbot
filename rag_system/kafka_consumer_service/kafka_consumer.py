from kafka import KafkaConsumer
import json
from vectorstore.index_builder import rebuild_index


def safe_json_deserializer(x):
    if x is None:
        return None
    try:
        return json.loads(x.decode("utf-8"))
    except json.JSONDecodeError:
        print("❌ Invalid JSON message:", x)
        return None


consumer = KafkaConsumer(
    "pdf_uploaded",
    bootstrap_servers="localhost:9092",
    value_deserializer=safe_json_deserializer,
    auto_offset_reset="earliest",
    group_id="latest"

)

for msg in consumer:
    if not msg.value:
        print("⚠️ Skipping empty Kafka message")
        continue

    event = msg.value

    if "filename" not in event:
        print("⚠️ Invalid message format:", event)
        continue

    print(f"🚀 START processing: {event['filename']}")
    rebuild_index()
    print(f"✅ FINISHED processing: {event['filename']}")
    