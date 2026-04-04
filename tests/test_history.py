"""Tests unitarios para el historial."""

import json
import os
import tempfile
import pytest

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.history import HistoryManager, CalculationRecord


@pytest.fixture
def temp_history():
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        path = f.name
    history = HistoryManager(file_path=path)
    yield history
    if os.path.exists(path):
        os.remove(path)


class TestHistoryManager:
    def test_add_record(self, temp_history):
        record = temp_history.add("2 + 2", "4", "deg")
        assert record.expression == "2 + 2"
        assert record.result == "4"
        assert record.mode == "deg"
        assert len(temp_history) == 1

    def test_get_all(self, temp_history):
        temp_history.add("1 + 1", "2")
        temp_history.add("2 + 2", "4")
        records = temp_history.get_all()
        assert len(records) == 2

    def test_get_last(self, temp_history):
        for i in range(5):
            temp_history.add(str(i), str(i))
        last_two = temp_history.get_last(2)
        assert len(last_two) == 2
        assert last_two[0].expression == "3"

    def test_clear(self, temp_history):
        temp_history.add("1 + 1", "2")
        temp_history.clear()
        assert len(temp_history) == 0

    def test_remove(self, temp_history):
        temp_history.add("1 + 1", "2")
        temp_history.add("2 + 2", "4")
        assert temp_history.remove(0) is True
        assert len(temp_history) == 1

    def test_remove_invalid(self, temp_history):
        assert temp_history.remove(99) is False

    def test_search(self, temp_history):
        temp_history.add("sin(30)", "0.5")
        temp_history.add("cos(60)", "0.5")
        temp_history.add("2 + 2", "4")
        results = temp_history.search("sin")
        assert len(results) == 1
        assert results[0].expression == "sin(30)"

    def test_persistence(self, temp_history):
        temp_history.add("5 * 5", "25")
        history2 = HistoryManager(file_path=temp_history.file_path)
        assert len(history2) == 1
        assert history2.records[0].expression == "5 * 5"

    def test_export_to_text(self, temp_history):
        temp_history.add("1 + 1", "2")
        content = temp_history.export_to_text()
        assert "1 + 1 = 2" in content

    def test_record_to_dict(self):
        record = CalculationRecord("1+1", "2", "2024-01-01", "deg")
        d = record.to_dict()
        assert d["expression"] == "1+1"
        assert d["result"] == "2"

    def test_record_from_dict(self):
        data = {
            "expression": "2*2",
            "result": "4",
            "timestamp": "2024-01-01",
            "mode": "deg",
        }
        record = CalculationRecord.from_dict(data)
        assert record.expression == "2*2"
