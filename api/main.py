from fastapi import FastAPI, HTTPException
import duckdb
import os
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Initialize FastAPI
app = FastAPI(
    title="⚡ SwiftHub Super App API",
    description="Operational Serving Layer for real-time transaction queries and user profiles.",
    version="1.0.0"
)

# DuckDB connection (Read-Only for API)
DB_PATH = "data/swifthub.duckdb"

def get_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Analytical warehouse not initialized. Run dbt build first.")
    return duckdb.connect(DB_PATH, read_only=True)

# Response Schemas
class UserProfile(BaseModel):
    user_id: str
    name: str
    loyalty_tier: str
    city: str
    churn_risk_score: float

class TransactionRecord(BaseModel):
    transaction_id: str
    transaction_timestamp: datetime
    total_amount: float
    department: str
    city: str

@app.get("/")
def root():
    return {
        "project": "SwiftHub Super App",
        "status": "Operational",
        "documentation": "/docs",
        "endpoints": ["/users/{id}", "/transactions/recent"]
    }

@app.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: str):
    """Retrieve a specific user's high-fidelity profile from the dim_users mart."""
    con = get_db()
    try:
        result = con.execute("SELECT * FROM dim_users WHERE user_id = ?", [user_id]).df()
        if result.empty:
            raise HTTPException(status_code=404, detail="User not found")
        return result.to_dict(orient="records")[0]
    finally:
        con.close()

@app.get("/transactions/recent", response_model=List[TransactionRecord])
def get_recent_transactions(limit: int = 10):
    """Fetch the latest transactions from the fct_transactions fact table."""
    con = get_db()
    try:
        result = con.execute(f"SELECT * FROM fct_transactions ORDER BY transaction_timestamp DESC LIMIT {limit}").df()
        return result.to_dict(orient="records")
    finally:
        con.close()

@app.get("/health")
def health():
    return {"status": "healthy", "warehouse": "connected" if os.path.exists(DB_PATH) else "offline"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
