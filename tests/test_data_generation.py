import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from generate_transactions import is_peak_hour
from generate_entities import get_region

def test_is_peak_hour():
    assert is_peak_hour(8) == True
    assert is_peak_hour(18) == True
    assert is_peak_hour(12) == False
    assert is_peak_hour(3) == False

def test_get_region():
    assert get_region("Jakarta") == "DKI Jakarta"
    assert get_region("Surabaya") == "Jawa Timur"
    assert get_region("Gotham") == "Unknown"
