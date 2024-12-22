import os
from app.kafka_settings.consumer import consume_topic
from app.service.process_service import process_event
from dotenv import load_dotenv

load_dotenv(verbose=True)

topic = os.environ["MONGO_TOPIC"]

if __name__ == '__main__':
    consume_topic(topic, process_event)