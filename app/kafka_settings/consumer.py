import json
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

from app.service.event_service import convert_to_mongo_compatible

load_dotenv(verbose=True)

bootstrap_servers = os.environ["BOOTSTRAP_SERVERS"]


def consume_topic(topic, process_message):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    for message in consumer:
        for event in message.value:
            event = convert_to_mongo_compatible(event)

            if event:
                process_message(event)
                print("Validated Event: ")
            else:
                print("Event validation failed.")
