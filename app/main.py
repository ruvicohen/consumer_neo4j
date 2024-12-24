import os
from app.kafka_settings.consumer import consume_topic
from dotenv import load_dotenv

from app.service.processing_load import process_event

load_dotenv(verbose=True)

topic = os.environ["DB_TOPIC"]

if __name__ == "__main__":
    consume_topic(topic, process_event)
