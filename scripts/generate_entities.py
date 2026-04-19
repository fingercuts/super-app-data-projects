import pandas as pd
import numpy as np
from faker import Faker
import json
import os
from config import *
from logger import logger
from schemas import UserContract, DriverContract, MerchantContract
from pydantic import ValidationError

fake = Faker('id_ID')
Faker.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def get_region(city):
    regions = {
        "Jakarta": "DKI Jakarta",
        "Surabaya": "Jawa Timur",
        "Bandung": "Jawa Barat",
        "Semarang": "Jawa Tengah",
        "Yogyakarta": "DI Yogyakarta",
        "Denpasar": "Bali",
        "Medan": "Sumatera Utara",
        "Palembang": "Sumatera Selatan"
    }
    return regions.get(city, "Unknown")

def save_to_dlq(entity_name, invalid_records):
    if not invalid_records:
        return
    dlq_path = os.path.join(DLQ_DIR, f"{entity_name}_dlq.json")
    with open(dlq_path, 'a') as f:
        for r in invalid_records:
            # Clean errors object for json serialization
            r['errors'] = str(r['errors'])
            f.write(json.dumps(r) + "\n")
    logger.warning(f"Sent {len(invalid_records)} bad records to DLQ: {dlq_path}")

def generate_users():
    logger.info("Generating users...")
    users = []
    dlq = []
    for i in range(1, NUM_USERS + 1):
        city = str(np.random.choice(CITIES, p=CITY_PROBS))
        loyalty_tier = str(np.random.choice(["Silver", "Gold", "Platinum"], p=[0.7, 0.2, 0.1]))
        churn_risk = max(0.0, min(1.0, np.random.normal(0.2, 0.1) if loyalty_tier != "Platinum" else np.random.normal(0.05, 0.02)))
        
        user_dict = {
            "user_id": f"U{i:06d}",
            "name": fake.name(),
            "gender": str(np.random.choice(["Male", "Female"], p=[0.5, 0.5])),
            "age": int(np.clip(int(np.random.normal(28, 8)), 15, 75)), 
            "city": city,
            "region": get_region(city),
            "loyalty_tier": loyalty_tier,
            "churn_risk_score": float(round(churn_risk, 4))
        }

        try:
            valid_user = UserContract(**user_dict)
            users.append(valid_user.model_dump())
        except ValidationError as e:
            dlq.append({"payload": user_dict, "errors": e.errors()})

    df = pd.DataFrame(users)
    df.to_parquet(os.path.join(OUTPUT_DIR, "users.parquet"), index=False)
    save_to_dlq("users", dlq)
    logger.info(f"Generated {len(users)} users successfully.")

def generate_drivers():
    logger.info("Generating drivers...")
    drivers = []
    dlq = []
    for i in range(1, NUM_DRIVERS + 1):
        city = str(np.random.choice(CITIES, p=CITY_PROBS))
        driver_dict = {
            "driver_id": f"D{i:05d}",
            "name": fake.name(),
            "gender": str(np.random.choice(["Male", "Female"], p=[0.85, 0.15])),
            "age": int(np.clip(int(np.random.normal(35, 10)), 18, 65)),
            "city": city,
            "vehicle_type": str(np.random.choice(["Motorcycle", "Car"], p=[0.8, 0.2])),
            "rating": float(round(np.random.uniform(3.5, 5.0), 1))
        }

        try:
            valid_driver = DriverContract(**driver_dict)
            drivers.append(valid_driver.model_dump())
        except ValidationError as e:
            dlq.append({"payload": driver_dict, "errors": e.errors()})

    df = pd.DataFrame(drivers)
    df.to_parquet(os.path.join(OUTPUT_DIR, "drivers.parquet"), index=False)
    save_to_dlq("drivers", dlq)
    logger.info(f"Generated {len(drivers)} drivers successfully.")

def generate_merchants():
    logger.info("Generating merchants...")
    merchants = []
    dlq = []
    for i in range(1, NUM_MERCHANTS + 1):
        city = str(np.random.choice(CITIES, p=CITY_PROBS))
        service_type = str(np.random.choice(["Food Delivery", "Grocery"], p=[0.8, 0.2]))
        dept = "Foodora" if service_type == "Food Delivery" else "QuickMart"
        merchant_dict = {
            "merchant_id": f"M{i:05d}",
            "merchant_name": fake.company(),
            "service_type": service_type,
            "department": dept,
            "city": city,
            "rating": float(round(np.random.uniform(3.0, 5.0), 1))
        }

        try:
            valid = MerchantContract(**merchant_dict)
            merchants.append(valid.model_dump())
        except ValidationError as e:
            dlq.append({"payload": merchant_dict, "errors": e.errors()})

    df = pd.DataFrame(merchants)
    df.to_parquet(os.path.join(OUTPUT_DIR, "merchants.parquet"), index=False)
    save_to_dlq("merchants", dlq)
    logger.info(f"Generated {len(merchants)} merchants successfully.")

def generate_services_and_promos():
    with open(os.path.join(OUTPUT_DIR, "services.json"), "w") as f:
        json.dump(SERVICES, f, indent=4)
    logger.info("Generated services.json")

    promotions = [
        {"promotion_id": "P-WELCOME", "promotion_name": "Welcome Bonus", "campaign_type": "New User", "discount_percentage": 0.5, "start_date": "2024-01-01", "end_date": "2024-12-31"},
        {"promotion_id": "P-HARBOLNAS", "promotion_name": "Harbolnas 11.11", "campaign_type": "Seasonal", "discount_percentage": 0.3, "start_date": "2024-11-10", "end_date": "2024-11-12"},
        {"promotion_id": "P-LEBARAN", "promotion_name": "Lebaran Feast", "campaign_type": "Holiday", "discount_percentage": 0.25, "start_date": "2024-04-01", "end_date": "2024-04-15"}
    ]
    with open(os.path.join(OUTPUT_DIR, "promotions.json"), "w") as f:
        json.dump(promotions, f, indent=4)
    logger.info("Generated promotions.json")

if __name__ == "__main__":
    generate_users()
    generate_drivers()
    generate_merchants()
    generate_services_and_promos()
