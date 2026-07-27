"""
generate_transactions.py - Sample transaction data generator.

This is the SAMPLE generator committed to the repo for reproducibility.
For production-scale data generation (millions of rows), use generate_bulk.py
which is kept in .gitignore to avoid bloating the repository.

Run: python scripts/generate_transactions.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import uuid
import json
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import *
from logger import logger
from schemas import TransactionContract
from pydantic import ValidationError

np.random.seed(RANDOM_SEED)

def generate_transactions():
    """Generate a small sample transaction dataset (1000 rows)."""
    logger.info("Generating sample transactions...")
    
    try:
        users_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "users.parquet"))
        drivers_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "drivers.parquet"))
        merchants_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "merchants.parquet"))
        with open(os.path.join(OUTPUT_DIR, "services.json"), "r") as f:
            services = json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Missing entity data. Please run generate_entities.py first. {e}")
        # Generate minimal fallback data
        logger.info("Creating fallback entity data...")
        _create_fallback_entities()
        users_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "users.parquet"))
        drivers_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "drivers.parquet"))
        merchants_df = pd.read_parquet(os.path.join(OUTPUT_DIR, "merchants.parquet"))
        with open(os.path.join(OUTPUT_DIR, "services.json"), "r") as f:
            services = json.load(f)

    n = NUM_TRANSACTIONS
    start_date = datetime.strptime(START_DATE_STR, "%Y-%m-%d")
    end_date = datetime.strptime(END_DATE_STR, "%Y-%m-%d")
    total_seconds = int((end_date - start_date).total_seconds())

    logger.info(f"Generating {n} transactions...")
    
    # Transaction IDs
    trx_ids = [f"TX{i:08d}" for i in range(1, n + 1)]
    
    # Random Datetimes
    random_seconds = np.random.randint(0, total_seconds, n)
    dates = start_date + pd.to_timedelta(random_seconds, unit='s')
    
    # Users Mapping
    user_choices = np.random.choice(users_df['user_id'].values, n)
    city_map = users_df.set_index('user_id')['city'].to_dict()
    region_map = users_df.set_index('user_id')['region'].to_dict()
    cities = np.array([city_map.get(u, "Jakarta") for u in user_choices])
    regions = np.array([region_map.get(u, "DKI Jakarta") for u in user_choices])

    # Services Setup
    service_probs = [0.35, 0.15, 0.15, 0.10, 0.10, 0.05, 0.10]
    svc_choices = np.random.choice([s['service_id'] for s in services], n, p=service_probs)
    
    dept_map = {s['service_id']: s['department'] for s in services}
    departments = np.array([dept_map.get(s, "Unknown") for s in svc_choices])

    # Assign drivers/merchants where necessary
    requires_driver = np.isin(departments, ["RideWay", "Foodora", "QuickMart", "ParcelPro"])
    requires_merchant = np.isin(departments, ["Foodora", "QuickMart"])
    
    driver_ids = np.where(requires_driver, np.random.choice(drivers_df['driver_id'].values, n), None)
    merchant_ids = np.where(requires_merchant, np.random.choice(merchants_df['merchant_id'].values, n), None)

    # Base Amounts
    base_amounts = np.zeros(n)
    hours = dates.hour if hasattr(dates, 'hour') else dates.dt.hour
    is_peak = ((hours >= 7) & (hours <= 9)) | ((hours >= 17) & (hours <= 19))
    
    ride_mask = departments == "RideWay"
    food_mask = np.isin(departments, ["Foodora", "QuickMart"])
    other_mask = ~(ride_mask | food_mask)

    base_amounts[ride_mask] = np.random.normal(30000, 10000, ride_mask.sum())
    base_amounts[ride_mask & is_peak] *= 1.5

    quantities = np.ones(n, dtype=int)
    food_qty = np.random.randint(1, 5, food_mask.sum())
    quantities[food_mask] = food_qty
    base_amounts[food_mask] = np.random.normal(50000, 20000, food_mask.sum()) * food_qty

    base_amounts[other_mask] = np.random.normal(15000, 5000, other_mask.sum())
    base_amounts = np.clip(base_amounts, 10000, None).astype(int)

    # Discounts
    promo_mask = np.random.rand(n) < 0.2
    discounts = np.zeros(n, dtype=int)
    discounts[promo_mask] = (base_amounts[promo_mask] * 0.5).astype(int)
    promo_ids = np.where(promo_mask, "P-WELCOME", None)

    total_amounts = base_amounts - discounts
    
    # Payments
    payment_methods = np.random.choice(["PayLink Wallet", "Credit Card", "Cash"], n, p=[0.6, 0.3, 0.1])
    
    logger.info("Constructing DataFrames...")
    df_trx = pd.DataFrame({
        "transaction_id": trx_ids,
        "date": dates.strftime('%Y-%m-%dT%H:%M:%S'),
        "user_id": user_choices,
        "driver_id": driver_ids,
        "merchant_id": merchant_ids,
        "service_id": svc_choices,
        "quantity": quantities,
        "base_amount": base_amounts,
        "discounted_amount": discounts,
        "total_amount": total_amounts,
        "payment_method": payment_methods,
        "department": departments,
        "city": cities,
        "region": regions,
        "promotion_id": promo_ids
    })

    df_payments = pd.DataFrame({
        "payment_id": [str(uuid.uuid4()) for _ in range(n)],
        "transaction_id": trx_ids,
        "payment_method": payment_methods,
        "amount": total_amounts,
        "status": np.random.choice(["SUCCESS", "FAILED"], n, p=[0.95, 0.05]),
        "date": (dates + pd.to_timedelta(np.random.randint(1, 5, n), unit='m')).strftime('%Y-%m-%dT%H:%M:%S')
    })

    # Geo-Spatial Map Clustering based on Cities realistically
    city_coords = {
        "Jakarta": (-6.2088, 106.8456), "Surabaya": (-7.2504, 112.7688),
        "Bandung": (-6.9175, 107.6191), "Denpasar": (-8.6500, 115.2167),
        "Medan": (3.5952, 98.6722), "Palembang": (-2.9909, 104.7566),
        "Semarang": (-6.9667, 110.4167), "Yogyakarta": (-7.7956, 110.3695)
    }
    
    base_lats = np.array([city_coords.get(c, (-6.2088, 106.8456))[0] for c in cities])
    base_longs = np.array([city_coords.get(c, (-6.2088, 106.8456))[1] for c in cities])
    
    df_locations = pd.DataFrame({
        "location_id": [str(uuid.uuid4()) for _ in range(n)],
        "transaction_id": trx_ids,
        "city": cities,
        "pickup_lat": base_lats + np.random.normal(0, 0.05, n),
        "pickup_long": base_longs + np.random.normal(0, 0.05, n),
        "dropoff_lat": base_lats + np.random.normal(0, 0.05, n),
        "dropoff_long": base_longs + np.random.normal(0, 0.05, n)
    })

    logger.info("Saving DataFrames to Parquet...")
    df_trx.to_parquet(os.path.join(OUTPUT_DIR, "transactions.parquet"), index=False)
    df_payments.to_parquet(os.path.join(OUTPUT_DIR, "payments.parquet"), index=False)
    df_locations.to_parquet(os.path.join(OUTPUT_DIR, "locations.parquet"), index=False)

    # SLA validation processing
    logger.info("Running SLA validation on generated transactions...")
    from scripts.sla_tracker import SLATracker
    
    tracker = SLATracker()
    results = []
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    
    # Validate a sample of rows (not all for performance)
    sample_size = min(100, len(df_trx))
    sample_indices = np.random.choice(len(df_trx), sample_size, replace=False)
    
    for idx in sample_indices:
        row = df_trx.iloc[idx]
        row_dict = row.to_dict()
        try:
            row_dict["date"] = datetime.strptime(row_dict["date"], "%Y-%m-%dT%H:%M:%S")
            TransactionContract(**row_dict)
            results.append({"status": "PASS", "check": "TransactionContract"})
        except ValidationError as e:
            results.append({
                "status": "FAIL", 
                "check": "TransactionContract", 
                "error": str(e).replace("\n", " ")
            })
            
    tracker.record_run(run_id, results)
    logger.info(f"SLA run recorded: {run_id} with {len(results)} validation checks.")
    logger.info("Sample transaction generation completed successfully.")

def _create_fallback_entities():
    """Create minimal fallback entity data if primary generators weren't run."""
    from faker import Faker
    fake = Faker('id_ID')
    fake.seed_instance(RANDOM_SEED)
    
    # Minimal users
    users_data = []
    for i in range(10):
        users_data.append({
            "user_id": f"U{i+1:06d}",
            "name": fake.name(),
            "gender": "Male" if i % 2 == 0 else "Female",
            "age": 25 + i,
            "city": "Jakarta",
            "region": "DKI Jakarta",
            "loyalty_tier": "Silver",
            "churn_risk_score": 0.1 + (i * 0.01)
        })
    pd.DataFrame(users_data).to_parquet(os.path.join(OUTPUT_DIR, "users.parquet"), index=False)
    
    # Minimal drivers
    drivers_data = []
    for i in range(5):
        drivers_data.append({
            "driver_id": f"D{i+1:05d}",
            "name": fake.name(),
            "gender": "Male",
            "age": 30 + i,
            "city": "Jakarta",
            "vehicle_type": "Motorcycle" if i % 2 == 0 else "Car",
            "rating": 4.0 + (i * 0.1)
        })
    pd.DataFrame(drivers_data).to_parquet(os.path.join(OUTPUT_DIR, "drivers.parquet"), index=False)
    
    # Minimal merchants
    merchants_data = []
    for i in range(5):
        merchants_data.append({
            "merchant_id": f"M{i+1:05d}",
            "merchant_name": fake.company(),
            "service_type": "Food Delivery" if i % 2 == 0 else "Grocery",
            "department": "Foodora" if i % 2 == 0 else "QuickMart",
            "city": "Jakarta",
            "rating": 4.0 + (i * 0.1)
        })
    pd.DataFrame(merchants_data).to_parquet(os.path.join(OUTPUT_DIR, "merchants.parquet"), index=False)
    
    logger.info("Created fallback entity data.")

if __name__ == "__main__":
    generate_transactions()
