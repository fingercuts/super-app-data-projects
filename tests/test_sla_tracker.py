import unittest
import tempfile
import os
import sqlite3
from scripts.sla_tracker import SLATracker

class TestSLATracker(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for database testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.tracker = SLATracker(db_path=self.db_path)

    def tearDown(self):
        # Close file descriptor and remove the temporary DB
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_database_initialization(self):
        """Verifies schema table is setup correctly."""
        self.assertTrue(os.path.exists(self.db_path))
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sla_runs'")
        table_exists = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table_exists)

    def test_record_and_stats_calculation(self):
        """Should save run and calculate appropriate averages."""
        mock_results = [
            {"status": "PASS", "check": "TestCheck"},
            {"status": "PASS", "check": "TestCheck"},
            {"status": "FAIL", "check": "TestCheck"}, # 2/3 passed = 66.67%
        ]
        
        self.tracker.record_run("RUN-TEST-001", mock_results)
        
        # Verify aggregates
        stats = self.tracker.get_aggregate_stats()
        self.assertEqual(stats["total_runs"], 1)
        self.assertEqual(stats["total_passed"], 2)
        self.assertEqual(stats["total_failed"], 1)
        self.assertEqual(stats["avg_sla"], 66.67)

    def test_empty_database_aggregates(self):
        """Should handle missing database records gracefully."""
        stats = self.tracker.get_aggregate_stats()
        self.assertEqual(stats["total_runs"], 0)
        self.assertEqual(stats["avg_sla"], 0.0)
        self.assertEqual(stats["total_passed"], 0)
        
        history = self.tracker.get_compliance_history()
        self.assertEqual(len(history), 0)
