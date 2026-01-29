"""Tests for ImportLog model."""
import pytest
from datetime import datetime, timezone
from museum_attendance_common.model import ImportLog
from museum_attendance_common.enumeration import ImportStatus


class TestImportLog:
    """Tests for ImportLog model."""

    def test_create_import_log(self):
        """Test creating an ImportLog."""
        log = ImportLog(
            status=ImportStatus.IN_PROGRESS.value,
            result=None
        )
        
        assert log.status == ImportStatus.IN_PROGRESS.value
        assert log.result is None

    def test_import_log_with_success_status(self):
        """Test ImportLog with SUCCESS status."""
        result = {"museums_imported": 50, "errors": 0}
        
        log = ImportLog(
            status=ImportStatus.SUCCESS.value,
            result=result
        )
        
        assert log.status == ImportStatus.SUCCESS.value
        assert log.result == result
        assert log.result["museums_imported"] == 50

    def test_import_log_with_failed_status(self):
        """Test ImportLog with FAILED status."""
        result = {"error": "Connection timeout", "museums_imported": 10}
        
        log = ImportLog(
            status=ImportStatus.FAILED.value,
            result=result
        )
        
        assert log.status == ImportStatus.FAILED.value
        assert log.result["error"] == "Connection timeout"

    def test_import_log_result_can_be_none(self):
        """Test that result can be None."""
        log = ImportLog(
            status=ImportStatus.IN_PROGRESS.value,
            result=None
        )
        
        assert log.result is None

    def test_import_log_attributes(self):
        """Test ImportLog attributes."""
        log = ImportLog(
            status=ImportStatus.SUCCESS.value,
            result={"total": 100}
        )
        log.id = 1
        
        assert log.id == 1
        assert log.status == ImportStatus.SUCCESS.value
        assert log.result == {"total": 100}

    def test_import_log_result_json_structure(self):
        """Test that result can hold complex JSON structure."""
        complex_result = {
            "museums": ["Louvre", "MET", "British Museum"],
            "stats": {
                "total": 100,
                "imported": 95,
                "failed": 5
            },
            "errors": [
                {"museum": "Test Museum", "error": "Invalid data"}
            ]
        }
        
        log = ImportLog(
            status=ImportStatus.SUCCESS.value,
            result=complex_result
        )
        
        assert log.result == complex_result
        assert log.result["museums"] == ["Louvre", "MET", "British Museum"]
        assert log.result["stats"]["imported"] == 95
        assert len(log.result["errors"]) == 1

    def test_import_log_status_enum_values(self):
        """Test that status can hold different enum values."""
        log1 = ImportLog(status=ImportStatus.IN_PROGRESS.value)
        log2 = ImportLog(status=ImportStatus.SUCCESS.value)
        log3 = ImportLog(status=ImportStatus.FAILED.value)
        
        assert log1.status == "IN_PROGRESS"
        assert log2.status == "SUCCESS"
        assert log3.status == "FAILED"
