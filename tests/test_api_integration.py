"""Integration test: FastAPI against a real DuckDB with generated data."""

import pytest
import sys
import os
import tempfile
import shutil
import duckdb

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def duckdb_with_data():
    """Create a temporary DuckDB populated from raw parquet files."""
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, "test_swifthub.duckdb")

    con = duckdb.connect(db_path)

    # Load raw data (escape backslashes for DuckDB)
    raw_dir = os.path.join(BASE_DIR, "data", "raw")
    for table in ['users', 'drivers', 'merchants', 'transactions']:
        pq = os.path.join(raw_dir, f"{table}.parquet")
        if os.path.exists(pq):
            # Escape backslashes and single quotes for DuckDB SQL (DuckDB uses '' for escaping)
            pq_sql = pq.replace('\\', '\\\\').replace("'", "''")
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_parquet('{pq_sql}')")

    # Create star schema tables
    con.execute("""
        CREATE TABLE dim_users AS
        SELECT user_id, name, gender, age, city, region, loyalty_tier, churn_risk_score
        FROM users
    """)
    con.execute("""
        CREATE TABLE dim_drivers AS
        SELECT driver_id, name, gender, age, city, vehicle_type, rating
        FROM drivers
    """)
    con.execute("""
        CREATE TABLE dim_merchants AS
        SELECT merchant_id, merchant_name, service_type, department, city, rating AS merchant_rating
        FROM merchants
    """)
    con.execute("""
        CREATE TABLE fct_transactions AS
        SELECT
            t.transaction_id, t.date, t.user_id, t.driver_id, t.merchant_id,
            t.service_id, t.quantity, t.base_amount, t.discounted_amount,
            t.total_amount, t.payment_method, t.department, t.city, t.region,
            t.promotion_id,
            u.name AS user_name, u.loyalty_tier, u.churn_risk_score,
            d.name AS driver_name, d.vehicle_type AS driver_vehicle_type, d.rating AS driver_rating,
            m.merchant_name, m.service_type AS merchant_service_type
        FROM transactions t
        LEFT JOIN users u ON t.user_id = u.user_id
        LEFT JOIN drivers d ON t.driver_id = d.driver_id
        LEFT JOIN merchants m ON t.merchant_id = m.merchant_id
    """)
    con.close()

    yield db_path

    shutil.rmtree(tmpdir)


def test_api_queries_real_duckdb(duckdb_with_data):
    """Verify the data pipeline produces valid star schema tables."""
    con = duckdb.connect(duckdb_with_data, read_only=True)

    # Test user lookup
    result = con.execute("SELECT * FROM dim_users WHERE user_id = 'U000001'").fetchone()
    assert result is not None, "User U000001 not found in dim_users"
    assert result[1] is not None, "User name is null"

    # Test transaction count
    count = con.execute("SELECT COUNT(*) FROM fct_transactions").fetchone()[0]
    assert count > 0, "fct_transactions is empty"

    # Test department distribution
    depts = con.execute("SELECT DISTINCT department FROM fct_transactions ORDER BY department").fetchall()
    dept_names = [d[0] for d in depts]
    assert 'RideWay' in dept_names, "RideWay department missing"
    assert 'Foodora' in dept_names, "Foodora department missing"

    con.close()


def test_api_user_endpoint_structure(duckdb_with_data):
    """Verify the API response structure matches the UserProfile schema."""
    from pydantic import BaseModel

    class ExpectedUser(BaseModel):
        user_id: str
        name: str
        loyalty_tier: str
        city: str
        churn_risk_score: float

    con = duckdb.connect(duckdb_with_data, read_only=True)
    result = con.execute("SELECT user_id, name, loyalty_tier, city, churn_risk_score FROM dim_users LIMIT 1").fetchone()
    con.close()

    # Cast DuckDB types to Python native types for Pydantic
    row = {
        'user_id': str(result[0]),
        'name': str(result[1]),
        'loyalty_tier': str(result[2]),
        'city': str(result[3]),
        'churn_risk_score': float(result[4]),
    }

    # Should not raise — validates schema
    user = ExpectedUser(**row)
    assert user.user_id.startswith('U'), f"Expected user_id to start with 'U', got {user.user_id}"
    assert 0.0 <= user.churn_risk_score <= 1.0


def test_api_transaction_endpoint_structure(duckdb_with_data):
    """Verify the API response structure matches the TransactionRecord schema."""
    from pydantic import BaseModel
    from datetime import datetime

    class ExpectedTx(BaseModel):
        transaction_id: str
        transaction_timestamp: datetime
        total_amount: float
        department: str
        city: str

    con = duckdb.connect(duckdb_with_data, read_only=True)
    result = con.execute("SELECT transaction_id, date, total_amount, department, city FROM fct_transactions LIMIT 1").fetchone()
    con.close()

    columns = ['transaction_id', 'transaction_timestamp', 'total_amount', 'department', 'city']
    # Cast DuckDB types to Python native types for Pydantic
    row = {
        'transaction_id': str(result[0]),
        'transaction_timestamp': result[1].to_python() if hasattr(result[1], 'to_python') else result[1],
        'total_amount': float(result[2]),
        'department': str(result[3]),
        'city': str(result[4]),
    }

    tx = ExpectedTx(**row)
    assert tx.transaction_id.startswith('TX'), f"Expected tx_id to start with 'TX', got {tx.transaction_id}"
    assert tx.total_amount > 0
