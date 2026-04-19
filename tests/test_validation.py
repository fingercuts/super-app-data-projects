import pytest
from datetime import datetime
from pydantic import ValidationError
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from schemas import TransactionContract, UserContract

def test_valid_user():
    user = UserContract(
        user_id="U000001",
        name="Test User",
        gender="Male",
        age=30,
        city="Jakarta",
        region="DKI Jakarta",
        loyalty_tier="Gold",
        churn_risk_score=0.1
    )
    assert user.user_id == "U000001"

def test_invalid_user_age():
    with pytest.raises(ValidationError):
        UserContract(
            user_id="U000001",
            name="Test User",
            gender="Male",
            age=-5,  # Invalid
            city="Jakarta",
            region="DKI Jakarta",
            loyalty_tier="Gold",
            churn_risk_score=0.1
        )

def test_valid_transaction():
    trx = TransactionContract(
        transaction_id="TX00000001",
        date=datetime.now(),
        user_id="U001",
        driver_id="D001",
        merchant_id=None,
        service_id="SRV-01",
        quantity=1,
        base_amount=50000,
        discounted_amount=10000,
        total_amount=40000,
        payment_method="Cash",
        department="RideWay",
        city="Jakarta",
        region="DKI Jakarta",
        promotion_id="P-01"
    )
    assert trx.total_amount == 40000

def test_invalid_transaction_math():
    with pytest.raises(ValidationError) as exc_info:
        TransactionContract(
            transaction_id="TX00000001",
            date=datetime.now(),
            user_id="U001",
            driver_id="D001",
            merchant_id=None,
            service_id="SRV-01",
            quantity=1,
            base_amount=50000,
            discounted_amount=10000,
            total_amount=50000, # Should be 40000, this will fail
            payment_method="Cash",
            department="RideWay",
            city="Jakarta",
            region="DKI Jakarta",
            promotion_id="P-01"
        )
    assert "total_amount must equal base_amount - discounted_amount" in str(exc_info.value)
