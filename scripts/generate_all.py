"""
generate_all.py - Orchestrates the full sample data generation pipeline.

This is the committed version that calls the sample generators.
For production-scale generation, use generate_bulk.py (excluded from git).

Usage: python scripts/generate_all.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_entities import generate_users, generate_drivers, generate_merchants, generate_services_and_promos
from generate_transactions import generate_transactions
from generate_dirty_data import simulate_dirty_data_pipeline
from logger import logger

if __name__ == "__main__":
    logger.info("Starting Enterprise Data Generation Pipeline...")
    
    generate_users()
    generate_drivers()
    generate_merchants()
    generate_services_and_promos()
    
    generate_transactions()
    
    simulate_dirty_data_pipeline()
    
    logger.info("Pipeline Completed Successfully!")
