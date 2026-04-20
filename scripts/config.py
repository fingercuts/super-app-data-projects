import os

# Platform-wide Deterministic Settings
RANDOM_SEED = 42

# Operational Parameters
NUM_USERS = 500
NUM_DRIVERS = 100
NUM_MERCHANTS = 50
NUM_TRANSACTIONS = 1000

# Geographic Targets (Indonesia)
CITIES = ["Jakarta", "Surabaya", "Bandung", "Semarang", "Yogyakarta", "Denpasar", "Medan", "Palembang"]
CITY_PROBS = [0.4, 0.15, 0.1, 0.08, 0.07, 0.05, 0.08, 0.07]

# Date Configurations
START_DATE_STR = "2024-01-01"
END_DATE_STR = "2024-12-31"

# Directory Structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "raw")
DLQ_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "production", "dlq")

# Infrastructure Endpoints
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC_TRANSACTIONS = "swifthub_transactions_unified"

# Service Ecosystem Definitions
SERVICES = [
    {"service_id": "RW-01", "service_name": "RideWay Go", "department": "RideWay"},
    {"service_id": "RW-02", "service_name": "RideWay Car", "department": "RideWay"},
    {"service_id": "FD-01", "service_name": "Foodora Express", "department": "Foodora"},
    {"service_id": "QM-01", "service_name": "QuickMart Essentials", "department": "QuickMart"},
    {"service_id": "PP-01", "service_name": "ParcelPro Express", "department": "ParcelPro"},
    {"service_id": "PL-01", "service_name": "PayLink Wallet", "department": "PayLink"},
    {"service_id": "LC-01", "service_name": "LifeConnect Shopping", "department": "LifeConnect"}
]
