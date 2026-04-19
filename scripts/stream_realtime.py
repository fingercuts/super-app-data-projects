import pandas as pd
import numpy as np
from datetime import datetime
import os
import time
import json
import uuid
from confluent_kafka import Producer

from config import *
from logger import logger
from schemas import TransactionContract
from pydantic import ValidationError

np.random.seed() # Randomize without a fixed seed for continuous running

def is_peak_hour(hour):
    return (7 <= hour <= 9) or (17 <= hour <= 19)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        # Just logging debug or trace here to avoid flooding terminal on high throughput
        pass

def stream_realtime_transactions():
    logger.info(f"Initializing Kafka Streamer to {KAFKA_BROKER} on topic {KAFKA_TOPIC_TRANSACTIONS}...")
    
    producer_conf = {'bootstrap.servers': KAFKA_BROKER}
    try:
        producer = Producer(producer_conf)
    except Exception as e:
        logger.critical(f"Failed to connect to Kafka Broker: {e}")
        return

    try:
        users_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "users.parquet"))
        drivers_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "drivers.parquet"))
        merchants_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "merchants.parquet"))
        with open(os.path.join(OUTPUT_DIR, "services.json"), "r") as f:
            services = json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Missing batch entity files: {e}. Please run a batch generation first.")
        return

    user_ids = users_df['user_id'].tolist()
    driver_ids = drivers_df['driver_id'].tolist()
    merchant_ids = merchants_df['merchant_id'].tolist()
    
    user_city_map = dict(zip(users_df['user_id'], users_df['city']))
    user_region_map = dict(zip(users_df['user_id'], users_df['region']))
    
    logger.info("Configuration loaded. Starting infinite live streaming loop...")
    transaction_count = 0

    try:
        while True:
            # Sleep 0.1 to 2.0 seconds to simulate natural traffic burst intervals
            sleep_time = np.random.uniform(0.1, 2.0)
            time.sleep(sleep_time)

            dt = datetime.now()
            hour = dt.hour
            trx_id = f"TX-LIVE-{uuid.uuid4().hex[:8].upper()}"
            
            user_id = np.random.choice(user_ids)
            service = np.random.choice(services)
            service_id = service['service_id']
            dept = service['department']
            
            driver_id = np.random.choice(driver_ids) if dept in ["RideWay", "Foodora", "QuickMart", "ParcelPro"] else None
            merchant_id = np.random.choice(merchant_ids) if dept in ["Foodora", "QuickMart"] else None
            
            quantity = 1
            if dept == "RideWay":
                base_amount = int(np.random.normal(35000, 10000))
                if is_peak_hour(hour):
                    base_amount = int(base_amount * 1.5)
            elif dept in ["Foodora", "QuickMart"]:
                base_amount = int(np.random.normal(55000, 20000))
                quantity = int(np.random.randint(1, 5))
                base_amount = base_amount * quantity
            else:
                base_amount = int(np.random.normal(20000, 5000))
                
            base_amount = max(15000, base_amount)
            discount = 0
            promo_id = None
            
            if np.random.rand() < 0.15:
                promo_id = "P-LIVE-FLASH"
                discount = int(base_amount * 0.4)
                
            total_amount = base_amount - discount
            
            trx_dict = {
                "transaction_id": trx_id,
                "date": dt,
                "user_id": user_id,
                "driver_id": driver_id,
                "merchant_id": merchant_id,
                "service_id": service_id,
                "quantity": quantity,
                "base_amount": base_amount,
                "discounted_amount": discount,
                "total_amount": total_amount,
                "payment_method": str(np.random.choice(["PayLink Wallet", "Credit Card", "Cash"], p=[0.7, 0.2, 0.1])),
                "department": dept,
                "city": user_city_map[user_id],
                "region": user_region_map[user_id],
                "promotion_id": promo_id
            }

            try:
                # Pydantic Enforcement
                valid_trx = TransactionContract(**trx_dict)
                payload = valid_trx.model_dump()
                payload['date'] = payload['date'].isoformat()
                
                # Push verified schema object directly to Kafka
                producer.poll(0)
                producer.produce(
                    KAFKA_TOPIC_TRANSACTIONS, 
                    value=json.dumps(payload).encode('utf-8'), 
                    callback=delivery_report
                )
                
                transaction_count += 1
                if transaction_count % 10 == 0:
                    logger.info(f"Streamed {transaction_count} live transactions to Event Bus...")

            except ValidationError as e:
                logger.warning(f"Live Stream Validation Dropped: {e}")
                
    except KeyboardInterrupt:
        logger.info("Streaming interrupted by user. Closing Kafka Producer...")
    finally:
        producer.flush()
        logger.info("Kafka Producer Flushed successfully.")

if __name__ == "__main__":
    stream_realtime_transactions()
