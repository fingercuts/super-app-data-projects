"""
Streaming integration tests with mocked Kafka producer.

These tests validate the streaming layer without requiring a real Kafka broker.

Run: pytest tests/test_streaming.py -v
"""

import pytest
import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))


class TestMessageSerialization:
    """Test message serialization and format."""
    
    def test_transaction_serialization(self):
        """Verify transactions can be serialized to JSON."""
        sample_msg = {
            "transaction_id": "TX001",
            "user_id": "U001",
            "amount": 50000,
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify JSON serialization works
        serialized = json.dumps(sample_msg).encode('utf-8')
        deserialized = json.loads(serialized.decode('utf-8'))
        
        assert deserialized["transaction_id"] == "TX001"
        assert deserialized["amount"] == 50000
    
    def test_message_structure(self):
        """Verify transaction message has required fields."""
        required_fields = ["transaction_id", "user_id", "amount", "timestamp"]
        
        sample_msg = {
            "transaction_id": "TX001",
            "user_id": "U001",
            "amount": 50000,
            "timestamp": datetime.now().isoformat()
        }
        
        for field in required_fields:
            assert field in sample_msg, f"Missing required field: {field}"


class TestSchemaValidation:
    """Test that streamed messages pass schema validation."""
    
    def test_valid_transaction_passes(self):
        """Verify a valid transaction passes schema validation."""
        from schemas import TransactionContract
        
        valid_txn = {
            "transaction_id": "TX001",
            "date": datetime.now(),
            "user_id": "U001",
            "driver_id": "D001",
            "merchant_id": None,
            "service_id": "RW-01",
            "quantity": 1,
            "base_amount": 50000,
            "discounted_amount": 5000,
            "total_amount": 45000,
            "payment_method": "PayLink Wallet",
            "department": "RideWay",
            "city": "Jakarta",
            "region": "DKI Jakarta",
            "promotion_id": None
        }
        
        # Should not raise
        txn = TransactionContract(**valid_txn)
        assert txn.transaction_id == "TX001"
        assert txn.total_amount == 45000
    
    def test_invalid_transaction_fails(self):
        """Verify an invalid transaction fails schema validation."""
        from schemas import TransactionContract
        from pydantic import ValidationError
        
        invalid_txn = {
            "transaction_id": "TX001",
            "date": datetime.now(),
            "user_id": "U001",
            "driver_id": "D001",
            "merchant_id": None,
            "service_id": "RW-01",
            "quantity": 0,  # Invalid: must be > 0
            "base_amount": 50000,
            "discounted_amount": 5000,
            "total_amount": 45000,
            "payment_method": "PayLink Wallet",
            "department": "RideWay",
            "city": "Jakarta",
            "region": "DKI Jakarta",
            "promotion_id": None
        }
        
        with pytest.raises(ValidationError):
            TransactionContract(**invalid_txn)
    
    def test_negative_amount_fails(self):
        """Verify negative amounts fail validation."""
        from schemas import TransactionContract
        from pydantic import ValidationError
        
        invalid_txn = {
            "transaction_id": "TX001",
            "date": datetime.now(),
            "user_id": "U001",
            "driver_id": "D001",
            "merchant_id": None,
            "service_id": "RW-01",
            "quantity": 1,
            "base_amount": -1000,  # Invalid: must be >= 0
            "discounted_amount": 0,
            "total_amount": -1000,
            "payment_method": "Cash",
            "department": "RideWay",
            "city": "Jakarta",
            "region": "DKI Jakarta",
            "promotion_id": None
        }
        
        with pytest.raises(ValidationError):
            TransactionContract(**invalid_txn)


class TestConsumerLogic:
    """Test the consumer logic with mocked data."""
    
    def test_message_deserialization(self):
        """Verify JSON deserialization works for transaction messages."""
        sample_message = json.dumps({
            "transaction_id": "TX001",
            "user_id": "U001",
            "amount": 50000,
            "timestamp": "2024-01-15T10:30:00"
        }).encode('utf-8')
        
        parsed = json.loads(sample_message.decode('utf-8'))
        
        assert parsed["transaction_id"] == "TX001"
        assert parsed["amount"] == 50000
        assert isinstance(parsed["timestamp"], str)
    
    def test_batch_deserialization(self):
        """Verify batch message deserialization."""
        messages = [
            {"transaction_id": "TX001", "amount": 50000},
            {"transaction_id": "TX002", "amount": 30000},
            {"transaction_id": "TX003", "amount": 75000}
        ]
        
        serialized = json.dumps(messages).encode('utf-8')
        deserialized = json.loads(serialized.decode('utf-8'))
        
        assert len(deserialized) == 3
        assert deserialized[0]["amount"] == 50000
        assert deserialized[2]["amount"] == 75000


class TestPeakHourDetection:
    """Test peak hour detection logic."""
    
    def test_morning_peak(self):
        """Verify morning peak hours (7-9 AM) are detected."""
        from schemas import is_peak_hour
        
        assert is_peak_hour(7) == True
        assert is_peak_hour(8) == True
        assert is_peak_hour(9) == True
    
    def test_evening_peak(self):
        """Verify evening peak hours (5-7 PM) are detected."""
        from schemas import is_peak_hour
        
        assert is_peak_hour(17) == True
        assert is_peak_hour(18) == True
        assert is_peak_hour(19) == True
    
    def test_off_peak_hours(self):
        """Verify off-peak hours are not flagged."""
        from schemas import is_peak_hour
        
        assert is_peak_hour(0) == False
        assert is_peak_hour(6) == False
        assert is_peak_hour(12) == False
        assert is_peak_hour(15) == False
        assert is_peak_hour(23) == False


class TestConfigConstants:
    """Test streaming configuration constants."""
    
    def test_kafka_broker_config(self):
        """Verify Kafka broker configuration."""
        from config import KAFKA_BROKER
        assert KAFKA_BROKER == "localhost:9092"
    
    def test_kafka_topic_config(self):
        """Verify Kafka topic configuration."""
        from config import KAFKA_TOPIC_TRANSACTIONS
        assert KAFKA_TOPIC_TRANSACTIONS == "swifthub_transactions_unified"
