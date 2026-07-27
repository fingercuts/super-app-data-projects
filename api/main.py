from fastapi import FastAPI, HTTPException
import duckdb
import os
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="SwiftHub API",
    description="REST API for querying the SwiftHub analytics warehouse.",
    version="1.0.0"
)

DB_PATH = "data/swifthub.duckdb"

def get_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Warehouse not initialized. Run dbt run first.")
    return duckdb.connect(DB_PATH, read_only=True)

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
        "project": "SwiftHub",
        "status": "Operational",
        "documentation": "/docs",
        "endpoints": ["/users/{id}", "/transactions/recent"]
    }

@app.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: str):
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
