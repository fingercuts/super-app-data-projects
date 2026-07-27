import os
import sqlite3
import json
from datetime import datetime, timezone

class SLATracker:
    """Tracks data quality validation results in a local SQLite database."""
    
    def __init__(self, db_path=None):
        if db_path is None:
            data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
            os.makedirs(data_dir, exist_ok=True)
            self.db_path = os.path.join(data_dir, "sla_metrics.db")
        else:
            self.db_path = db_path
            
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sla_runs (
                run_id TEXT PRIMARY KEY,
                timestamp TEXT,
                total_checks INTEGER,
                passed_checks INTEGER,
                failed_checks INTEGER,
                pass_rate REAL,
                details_json TEXT
            )
        """)
        conn.commit()
        conn.close()

    def record_run(self, run_id: str, results: list):
        """Log a validation run's results to the database."""
        if not results:
            return
            
        total = len(results)
        passed = sum(1 for r in results if r.get("status") == "PASS")
        failed = total - passed
        pass_rate = (passed / total) * 100.0 if total > 0 else 0.0
        
        details_json = json.dumps(results)
        timestamp = datetime.now(timezone.utc).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sla_runs (run_id, timestamp, total_checks, passed_checks, failed_checks, pass_rate, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (run_id, timestamp, total, passed, failed, pass_rate, details_json))
        conn.commit()
        conn.close()

    def get_compliance_history(self, limit=30) -> list:
        """Return the most recent validation runs."""
        if not os.path.exists(self.db_path):
            return []
            
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT run_id, timestamp, total_checks, passed_checks, failed_checks, pass_rate
            FROM sla_runs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

    def get_aggregate_stats(self) -> dict:
        """Return overall pass rates across all validation runs."""
        if not os.path.exists(self.db_path):
            return {"avg_sla": 0.0, "total_runs": 0, "total_passed": 0, "total_failed": 0}
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*), SUM(total_checks), SUM(passed_checks), SUM(failed_checks)
            FROM sla_runs
        """)
        row = cursor.fetchone()
        conn.close()
        
        if not row or row[0] == 0:
            return {"avg_sla": 0.0, "total_runs": 0, "total_passed": 0, "total_failed": 0}
            
        total_runs = row[0]
        total_checks = row[1] or 0
        total_passed = row[2] or 0
        total_failed = row[3] or 0
        
        avg_sla = (total_passed / total_checks) * 100.0 if total_checks > 0 else 0.0
        
        return {
            "avg_sla": round(avg_sla, 2),
            "total_runs": total_runs,
            "total_passed": total_passed,
            "total_failed": total_failed
        }
