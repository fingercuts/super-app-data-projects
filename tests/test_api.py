import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Verify root endpoint returns the correct metadata and 200 status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "SwiftHub"
    assert data["status"] == "Operational"

def test_health_endpoint():
    """Verify health endpoint returns a healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@patch("api.main.get_db")
def test_get_user_profile_success(mock_get_db):
    """Test getting a user profile successfully with mock data."""
    # Set up mock DB cursor and DataFrame return value
    mock_con = MagicMock()
    mock_get_db.return_value = mock_con
    
    mock_df = pd.DataFrame([{
        "user_id": "USR-001",
        "name": "Budiman",
        "loyalty_tier": "Platinum",
        "city": "Jakarta",
        "churn_risk_score": 0.12
    }])
    mock_con.execute.return_value.df.return_value = mock_df

    response = client.get("/users/USR-001")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "USR-001"
    assert data["name"] == "Budiman"
    assert data["loyalty_tier"] == "Platinum"
    
    # Assert query executed with the correct parameter
    mock_con.execute.assert_called_once_with(
        "SELECT * FROM dim_users WHERE user_id = ?", ["USR-001"]
    )

@patch("api.main.get_db")
def test_get_user_profile_not_found(mock_get_db):
    """Verify 404 response when a user is not found."""
    mock_con = MagicMock()
    mock_get_db.return_value = mock_con
    
    mock_df = pd.DataFrame([]) # Empty search result
    mock_con.execute.return_value.df.return_value = mock_df

    response = client.get("/users/USR-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@patch("api.main.get_db")
def test_get_recent_transactions(mock_get_db):
    """Verify recent transactions return structured lists."""
    mock_con = MagicMock()
    mock_get_db.return_value = mock_con
    
    mock_df = pd.DataFrame([
        {
            "transaction_id": "TX-001",
            "transaction_timestamp": "2026-07-15T08:00:00",
            "total_amount": 15000.0,
            "department": "RideWay",
            "city": "Jakarta"
        },
        {
            "transaction_id": "TX-002",
            "transaction_timestamp": "2026-07-15T08:05:00",
            "total_amount": 42000.0,
            "department": "Foodora",
            "city": "Surabaya"
        }
    ])
    mock_con.execute.return_value.df.return_value = mock_df

    response = client.get("/transactions/recent?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["transaction_id"] == "TX-001"
    assert data[1]["department"] == "Foodora"
