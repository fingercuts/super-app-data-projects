"""
generate_dirty_data.py - Simulates dirty/corrupt data for DLQ testing.

This script generates intentionally malformed data to test the Pydantic
validation contracts and Dead Letter Queue (DLQ) routing.

Run: python scripts/generate_dirty_data.py
"""

import pandas as pd
import numpy as np
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *
from logger import logger
from schemas import UserContract, DriverContract, MerchantContract, TransactionContract
from pydantic import ValidationError

np.random.seed(RANDOM_SEED + 1)  # Different seed from clean data

def simulate_dirty_data_pipeline():
    """Generate dirty data and route valid records to production, invalid to DLQ."""
    logger.info("Starting dirty data simulation pipeline...")
    
    dlq_dir = DLQ_DIR
    os.makedirs(dlq_dir, exist_ok=True)
    
    # Clear previous DLQ files
    for f in os.listdir(dlq_dir):
        if f.endswith('.json'):
            os.remove(os.path.join(dlq_dir, f))
    
    dirty_users = _generate_dirty_users()
    dirty_drivers = _generate_dirty_drivers()
    dirty_merchants = _generate_dirty_merchants()
    dirty_transactions = _generate_dirty_transactions()
    
    logger.info(f"Dirty data simulation complete:")
    logger.info(f"  Users: {dirty_users['valid']} valid, {dirty_users['invalid']} invalid")
    logger.info(f"  Drivers: {dirty_drivers['valid']} valid, {dirty_drivers['invalid']} invalid")
    logger.info(f"  Merchants: {dirty_merchants['valid']} valid, {dirty_merchants['invalid']} invalid")
    logger.info(f"  Transactions: {dirty_transactions['valid']} valid, {dirty_transactions['invalid']} invalid")
    
    # Log summary stats
    total_invalid = sum([
        dirty_users['invalid'],
        dirty_drivers['invalid'],
        dirty_merchants['invalid'],
        dirty_transactions['invalid']
    ])
    logger.info(f"Total invalid records sent to DLQ: {total_invalid}")

def _generate_dirty_users():
    """Generate users with various types of data corruption."""
    valid_records = []
    invalid_records = []
    
    for i in range(20):
        # Every other record is dirty
        if i % 2 == 0:
            # Dirty: invalid age, wrong gender, out-of-range churn score
            dirty_user = {
                "user_id": f"DUP{i:04d}",
                "name": f"Dirty User {i}",
                "gender": "Non-binary",  # Invalid gender
                "age": 200,  # Out of range
                "city": "Jakarta",
                "region": "DKI Jakarta",
                "loyalty_tier": "Diamond",  # Invalid tier
                "churn_risk_score": 5.0  # Out of range (should be 0-1)
            }
            try:
                UserContract(**dirty_user)
                valid_records.append(dirty_user)
            except ValidationError as e:
                invalid_records.append({
                    "payload": dirty_user,
                    "errors": str(e)
                })
        else:
            # Valid record
            valid_user = {
                "user_id": f"DUP{i:04d}",
                "name": f"Valid User {i}",
                "gender": "Male" if i % 3 == 0 else "Female",
                "age": 25 + (i % 30),
                "city": "Jakarta",
                "region": "DKI Jakarta",
                "loyalty_tier": "Silver",
                "churn_risk_score": round(np.random.uniform(0, 0.5), 4)
            }
            valid_records.append(valid_user)
    
    _save_to_dlq("dirty_users", invalid_records)
    if valid_records:
        pd.DataFrame(valid_records).to_parquet(
            os.path.join(os.path.dirname(BASE_DIR), "data", "raw", "dirty_users.parquet"),
            index=False
        )
    
    return {"valid": len(valid_records), "invalid": len(invalid_records)}

def _generate_dirty_drivers():
    """Generate drivers with various types of data corruption."""
    valid_records = []
    invalid_records = []
    
    for i in range(15):
        if i % 3 == 0:
            # Dirty: negative age, invalid vehicle type
            dirty_driver = {
                "driver_id": f"DD{i:04d}",
                "name": f"Dirty Driver {i}",
                "gender": "Male",
                "age": -5,  # Invalid age
                "city": "Jakarta",
                "vehicle_type": "Bicycle",  # Invalid vehicle type
                "rating": 0.0  # Out of range
            }
            try:
                DriverContract(**dirty_driver)
                valid_records.append(dirty_driver)
            except ValidationError as e:
                invalid_records.append({
                    "payload": dirty_driver,
                    "errors": str(e)
                })
        else:
            valid_driver = {
                "driver_id": f"DD{i:04d}",
                "name": f"Valid Driver {i}",
                "gender": "Male",
                "age": 25 + (i % 30),
                "city": "Jakarta",
                "vehicle_type": "Motorcycle",
                "rating": round(np.random.uniform(3.5, 5.0), 1)
            }
            valid_records.append(valid_driver)
    
    _save_to_dlq("dirty_drivers", invalid_records)
    
    return {"valid": len(valid_records), "invalid": len(invalid_records)}

def _generate_dirty_merchants():
    """Generate merchants with various types of data corruption."""
    valid_records = []
    invalid_records = []
    
    for i in range(10):
        if i % 2 == 0:
            dirty_merchant = {
                "merchant_id": f"DM{i:04d}",
                "merchant_name": "",  # Empty name
                "service_type": "Taxi Service",  # Invalid service type
                "department": "Gojek",  # Invalid department
                "city": "Jakarta",
                "rating": 10.0  # Out of range
            }
            try:
                MerchantContract(**dirty_merchant)
                valid_records.append(dirty_merchant)
            except ValidationError as e:
                invalid_records.append({
                    "payload": dirty_merchant,
                    "errors": str(e)
                })
        else:
            valid_merchant = {
                "merchant_id": f"DM{i:04d}",
                "merchant_name": f"Merchant {i}",
                "service_type": "Food Delivery",
                "department": "Foodora",
                "city": "Jakarta",
                "rating": round(np.random.uniform(3.0, 5.0), 1)
            }
            valid_records.append(valid_merchant)
    
    _save_to_dlq("dirty_merchants", invalid_records)
    
    return {"valid": len(valid_records), "invalid": len(invalid_records)}

def _generate_dirty_transactions():
    """Generate transactions with various types of data corruption."""
    valid_records = []
    invalid_records = []
    
    for i in range(25):
        if i % 4 == 0:
            # Dirty: negative amounts, wrong math
            dirty_trx = {
                "transaction_id": f"DTX{i:04d}",
                "date": datetime.now(),
                "user_id": f"U{i:06d}",
                "driver_id": f"D{i:05d}",
                "merchant_id": None,
                "service_id": "RW-01",
                "quantity": 0,  # Invalid (should be > 0)
                "base_amount": -1000,  # Negative amount
                "discounted_amount": 500,
                "total_amount": 1000,  # Wrong math: should be base - discount
                "payment_method": "Cash",
                "department": "RideWay",
                "city": "Jakarta",
                "region": "DKI Jakarta",
                "promotion_id": None
            }
            try:
                TransactionContract(**dirty_trx)
                valid_records.append(dirty_trx)
            except ValidationError as e:
                invalid_records.append({
                    "payload": dirty_trx,
                    "errors": str(e)
                })
        else:
            valid_trx = {
                "transaction_id": f"DTX{i:04d}",
                "date": datetime.now(),
                "user_id": f"U{i:06d}",
                "driver_id": f"D{i:05d}" if i % 2 == 0 else None,
                "merchant_id": f"M{i:05d}" if i % 3 == 0 else None,
                "service_id": "RW-01",
                "quantity": 1,
                "base_amount": 30000,
                "discounted_amount": 5000,
                "total_amount": 25000,  # Correct math
                "payment_method": "PayLink Wallet",
                "department": "RideWay",
                "city": "Jakarta",
                "region": "DKI Jakarta",
                "promotion_id": "P-WELCOME" if i % 5 == 0 else None
            }
            valid_records.append(valid_trx)
    
    _save_to_dlq("dirty_transactions", invalid_records)
    
    return {"valid": len(valid_records), "invalid": len(invalid_records)}

def _save_to_dlq(entity_name, invalid_records):
    """Save invalid records to the Dead Letter Queue."""
    if not invalid_records:
        return
    
    dlq_path = os.path.join(DLQ_DIR, f"{entity_name}_dlq.json")
    with open(dlq_path, 'w') as f:
        for record in invalid_records:
            f.write(json.dumps(record, default=str) + "\n")
    
    logger.warning(f"Saved {len(invalid_records)} invalid {entity_name} records to DLQ: {dlq_path}")

if __name__ == "__main__":
    simulate_dirty_data_pipeline()
