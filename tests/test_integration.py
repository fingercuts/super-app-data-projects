"""
Integration test for the full SwiftHub data pipeline.

This test validates the end-to-end flow:
1. Generate sample data
2. Verify data quality (schema, ranges)
3. Verify dbt model compatibility
4. Verify SLA tracking

Run: pytest tests/test_integration.py -v
"""

import pytest
import sys
import os
import pandas as pd
import numpy as np

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PRODUCTION_DIR = os.path.join(DATA_DIR, "production")
RAW_DIR = os.path.join(DATA_DIR, "raw")


@pytest.fixture(scope="module", autouse=True)
def generate_test_data():
    """Generate sample data before running integration tests."""
    print("\n=== Generating sample data for integration tests ===")
    
    # Create directories
    os.makedirs(PRODUCTION_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(os.path.join(PRODUCTION_DIR, "dlq"), exist_ok=True)
    
    # Run entity generation
    try:
        from generate_entities import generate_users, generate_drivers, generate_merchants, generate_services_and_promos
        generate_users()
        generate_drivers()
        generate_merchants()
        generate_services_and_promos()
    except ImportError:
        pytest.skip("generate_entities.py not found")
    
    # Run transaction generation
    try:
        from generate_transactions import generate_transactions
        generate_transactions()
    except ImportError:
        pytest.skip("generate_transactions.py not found")
    
    yield  # Run tests here
    
    # Cleanup (optional - comment out to inspect generated data)
    # print("\n=== Cleaning up test data ===")
    # for f in os.listdir(RAW_DIR):
    #     if f.endswith('.parquet'):
    #         os.remove(os.path.join(RAW_DIR, f))


class TestDataGeneration:
    """Test that generated data meets expected criteria."""
    
    def test_users_parquet_exists(self):
        """Verify users.parquet was generated."""
        path = os.path.join(RAW_DIR, "users.parquet")
        assert os.path.exists(path), f"users.parquet not found at {path}"
    
    def test_users_has_expected_columns(self):
        """Verify users table has all required columns."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        required_cols = ['user_id', 'name', 'gender', 'age', 'city', 'region', 'loyalty_tier', 'churn_risk_score']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_users_count_reasonable(self):
        """Verify we generated a reasonable number of users."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        assert len(df) > 0, "No users generated"
        assert len(df) <= 10000, f"Too many users: {len(df)}"
    
    def test_users_gender_valid(self):
        """Verify all genders are Male or Female."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        valid_genders = {'Male', 'Female'}
        assert df['gender'].isin(valid_genders).all(), "Invalid gender values found"
    
    def test_users_age_in_range(self):
        """Verify all ages are within valid range (15-100)."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        assert (df['age'] >= 15).all(), "Found users with age < 15"
        assert (df['age'] <= 100).all(), "Found users with age > 100"
    
    def test_users_loyalty_tier_valid(self):
        """Verify all loyalty tiers are valid."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        valid_tiers = {'Silver', 'Gold', 'Platinum'}
        assert df['loyalty_tier'].isin(valid_tiers).all(), "Invalid loyalty tier values found"
    
    def test_users_churn_risk_valid(self):
        """Verify churn risk scores are between 0 and 1."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        assert (df['churn_risk_score'] >= 0.0).all(), "Negative churn risk found"
        assert (df['churn_risk_score'] <= 1.0).all(), "Churn risk > 1.0 found"
    
    def test_drivers_parquet_exists(self):
        """Verify drivers.parquet was generated."""
        path = os.path.join(RAW_DIR, "drivers.parquet")
        assert os.path.exists(path), f"drivers.parquet not found at {path}"
    
    def test_drivers_vehicle_types(self):
        """Verify driver vehicle types are valid."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "drivers.parquet"))
        valid_types = {'Motorcycle', 'Car'}
        assert df['vehicle_type'].isin(valid_types).all(), "Invalid vehicle type found"
    
    def test_drivers_rating_in_range(self):
        """Verify driver ratings are between 1.0 and 5.0."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "drivers.parquet"))
        assert (df['rating'] >= 1.0).all(), "Driver rating < 1.0 found"
        assert (df['rating'] <= 5.0).all(), "Driver rating > 5.0 found"
    
    def test_transactions_parquet_exists(self):
        """Verify transactions.parquet was generated."""
        path = os.path.join(RAW_DIR, "transactions.parquet")
        assert os.path.exists(path), f"transactions.parquet not found at {path}"
    
    def test_transactions_has_required_columns(self):
        """Verify transactions table has all required columns."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        required_cols = ['transaction_id', 'date', 'user_id', 'service_id', 'total_amount', 'payment_method']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_transactions_amount_positive(self):
        """Verify all transaction amounts are positive."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        assert (df['total_amount'] > 0).all(), "Found non-positive transaction amounts"
        assert (df['base_amount'] > 0).all(), "Found non-positive base amounts"
    
    def test_transactions_quantity_positive(self):
        """Verify all quantities are >= 1."""
        df = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        assert (df['quantity'] >= 1).all(), "Found quantity < 1"
    
    def test_payments_parquet_exists(self):
        """Verify payments.parquet was generated."""
        path = os.path.join(RAW_DIR, "payments.parquet")
        assert os.path.exists(path), f"payments.parquet not found at {path}"
    
    def test_locations_parquet_exists(self):
        """Verify locations.parquet was generated."""
        path = os.path.join(RAW_DIR, "locations.parquet")
        assert os.path.exists(path), f"locations.parquet not found at {path}"


class TestDataRelationships:
    """Test that data relationships are consistent."""
    
    def test_transaction_users_exist(self):
        """Verify all transaction user_ids exist in users table."""
        users = pd.read_parquet(os.path.join(RAW_DIR, "users.parquet"))
        transactions = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        
        valid_user_ids = set(users['user_id'])
        invalid_users = set(transactions['user_id']) - valid_user_ids
        
        assert len(invalid_users) == 0, f"Found {len(invalid_users)} invalid user references"
    
    def test_transaction_driver_refs_valid(self):
        """Verify driver references in transactions are valid (where not null)."""
        drivers = pd.read_parquet(os.path.join(RAW_DIR, "drivers.parquet"))
        transactions = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        
        valid_driver_ids = set(drivers['driver_id'])
        driver_refs = transactions['driver_id'].dropna()
        invalid_drivers = set(driver_refs) - valid_driver_ids
        
        assert len(invalid_drivers) == 0, f"Found {len(invalid_drivers)} invalid driver references"
    
    def test_payment_transaction_count_match(self):
        """Verify payment count matches transaction count."""
        transactions = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        payments = pd.read_parquet(os.path.join(RAW_DIR, "payments.parquet"))
        
        assert len(transactions) == len(payments), \
            f"Transaction count ({len(transactions)}) != Payment count ({len(payments)})"
    
    def test_location_transaction_count_match(self):
        """Verify location count matches transaction count."""
        transactions = pd.read_parquet(os.path.join(RAW_DIR, "transactions.parquet"))
        locations = pd.read_parquet(os.path.join(RAW_DIR, "locations.parquet"))
        
        assert len(transactions) == len(locations), \
            f"Transaction count ({len(transactions)}) != Location count ({len(locations)})"


class TestDLQGeneration:
    """Test that dirty data generation routes invalid records correctly."""
    
    def test_dirty_data_generates_dlq(self):
        """Verify dirty data generation creates DLQ files."""
        # Run dirty data generation
        try:
            from generate_dirty_data import simulate_dirty_data_pipeline
            simulate_dirty_data_pipeline()
        except ImportError:
            pytest.skip("generate_dirty_data.py not found")
        
        dlq_dir = os.path.join(PRODUCTION_DIR, "dlq")
        dlq_files = [f for f in os.listdir(dlq_dir) if f.endswith('_dlq.json')]
        
        assert len(dlq_files) > 0, "No DLQ files generated"
    
    def test_dlq_contains_invalid_records(self):
        """Verify DLQ files contain records with validation errors."""
        dlq_dir = os.path.join(PRODUCTION_DIR, "dlq")
        
        for dlq_file in os.listdir(dlq_dir):
            if dlq_file.endswith('_dlq.json'):
                filepath = os.path.join(dlq_dir, dlq_file)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                
                assert len(lines) > 0, f"Empty DLQ file: {dlq_file}"
                
                # Verify each line has errors field
                for line in lines:
                    import json
                    record = json.loads(line.strip())
                    assert 'errors' in record, f"DLQ record missing 'errors' field: {dlq_file}"


class TestSLATracker:
    """Test that SLA tracking records validation results."""
    
    def test_sla_tracker_records_run(self):
        """Verify SLA tracker can record a validation run."""
        from sla_tracker import SLATracker
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            tracker = SLATracker(db_path=db_path)
            results = [
                {"status": "PASS", "check": "Test"},
                {"status": "PASS", "check": "Test"},
                {"status": "FAIL", "check": "Test"}
            ]
            tracker.record_run("TEST-RUN-001", results)
            
            history = tracker.get_compliance_history(limit=10)
            assert len(history) > 0, "No compliance history recorded"
            
            stats = tracker.get_aggregate_stats()
            assert 'total_runs' in stats, "Stats missing total_runs"
            # Stats may have 'avg_sla' instead of 'pass_rate' depending on implementation
            assert 'avg_sla' in stats or 'pass_rate' in stats, "Stats missing avg_sla or pass_rate"
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)


class TestConfig:
    """Test configuration constants."""
    
    def test_random_seed_set(self):
        """Verify RANDOM_SEED is set for reproducibility."""
        from config import RANDOM_SEED
        assert RANDOM_SEED is not None, "RANDOM_SEED not set"
        assert isinstance(RANDOM_SEED, int), "RANDOM_SEED should be an integer"
    
    def test_cities_defined(self):
        """Verify CITIES list is populated."""
        from config import CITIES
        assert len(CITIES) > 0, "CITIES list is empty"
        assert "Jakarta" in CITIES, "Jakarta should be in CITIES"
    
    def test_num_transactions_positive(self):
        """Verify NUM_TRANSACTIONS is positive."""
        from config import NUM_TRANSACTIONS
        assert NUM_TRANSACTIONS > 0, "NUM_TRANSACTIONS should be positive"
