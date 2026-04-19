from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

class UserContract(BaseModel):
    user_id: str
    name: str
    gender: Literal["Male", "Female"]
    age: int = Field(ge=15, le=100)
    city: str
    region: str
    loyalty_tier: Literal["Silver", "Gold", "Platinum"]
    churn_risk_score: float = Field(ge=0.0, le=1.0)

class DriverContract(BaseModel):
    driver_id: str
    name: str
    gender: Literal["Male", "Female"]
    age: int = Field(ge=18, le=65)
    city: str
    vehicle_type: Literal["Motorcycle", "Car"]
    rating: float = Field(ge=1.0, le=5.0)

class MerchantContract(BaseModel):
    merchant_id: str
    merchant_name: str
    service_type: str
    department: str
    city: str
    rating: float = Field(ge=1.0, le=5.0)

class TransactionContract(BaseModel):
    transaction_id: str
    date: datetime
    user_id: str
    driver_id: Optional[str]
    merchant_id: Optional[str]
    service_id: str
    quantity: int = Field(gt=0)
    base_amount: int = Field(ge=0)
    discounted_amount: int = Field(ge=0)
    total_amount: int = Field(ge=0)
    payment_method: str
    department: str
    city: str
    region: str
    promotion_id: Optional[str]

    @field_validator('total_amount')
    @classmethod
    def check_total_logic(cls, v: int, info):
        if 'base_amount' in info.data and 'discounted_amount' in info.data:
            if v != (info.data['base_amount'] - info.data['discounted_amount']):
                raise ValueError("total_amount must equal base_amount - discounted_amount")
        return v
