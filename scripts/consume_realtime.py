import json
import logging
from confluent_kafka import Consumer, KafkaError, KafkaException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [KAFKA_CONSUMER] - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def consume_stream():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'swifthub_analytics_group',
        'auto.offset.reset': 'latest'
    }

    consumer = Consumer(conf)
    topic = 'swifthub.transactions.live'
    
    try:
        consumer.subscribe([topic])
        logger.info(f"Subscribed to topic: {topic}. Listening to real-time pub/sub stream...")

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: 
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            
            # Decode and process the payload
            payload = json.loads(msg.value().decode('utf-8'))
            amount = payload.get('total_amount', 0)
            dept = payload.get('department', 'UNKNOWN')
            
            # Simulated real-time processing (mock DB dump or notification alert)
            logger.info(f"[LIVE EVENT] -> Rp {amount:,.0f} | Dept: {dept} | Rider/Courier ID: {payload.get('driver_id')}")

    except KeyboardInterrupt:
        logger.info("Gracefully shutting down stream consumer...")
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_stream()
