"""Tests for ImportLogRepository."""
import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from museum_attendance_common.repository import ImportLogRepository
from museum_attendance_common.model import ImportLog
from museum_attendance_common.enumeration import ImportStatus


class TestImportLogRepository:
    """Tests for ImportLogRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def repository(self, mock_session):
        """Create an ImportLogRepository with mock session."""
        return ImportLogRepository(mock_session)

    def test_start_job(self, repository, mock_session):
        """Test starting a new import job."""
        result = repository.start_job(ImportStatus.IN_PROGRESS)
        
        assert isinstance(result, ImportLog)
        assert result.status == ImportStatus.IN_PROGRESS.value
        assert result.result is None
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    def test_start_job_with_result(self, repository, mock_session):
        """Test starting a job with initial result data."""
        initial_result = {"started": True}
        
        result = repository.start_job(ImportStatus.IN_PROGRESS, initial_result)
        
        assert result.result == initial_result

    def test_end_job_with_success(self, repository, mock_session):
        """Test ending a job with success status."""
        import_log = ImportLog(
            status=ImportStatus.IN_PROGRESS.value,
            result=None
        )
        import_log.id = 1
        result_data = {"museums_imported": 50, "errors": 0}
        
        result = repository.end_job_with_success(import_log, result_data)
        
        assert result.status == ImportStatus.SUCCESS.value
        assert result.result == result_data
        assert result.completed_at is not None
        mock_session.flush.assert_called_once()

    def test_end_job_with_success_no_result(self, repository, mock_session):
        """Test ending a job with success and no result data."""
        import_log = ImportLog(
            status=ImportStatus.IN_PROGRESS.value,
            result=None
        )
        import_log.id = 1
        
        result = repository.end_job_with_success(import_log, None)
        
        assert result.status == ImportStatus.SUCCESS.value
        assert result.result is None
        mock_session.flush.assert_called_once()

    def test_end_job_with_failure(self, repository, mock_session):
        """Test ending a job with failure status."""
        import_log = ImportLog(
            status=ImportStatus.IN_PROGRESS.value,
            result=None
        )
        import_log.id = 1
        result_data = {
            "error": "Connection timeout",
            "museums_imported": 10,
            "museums_failed": 40
        }
        
        result = repository.end_job_with_failure(import_log, result_data)
        
        assert result.status == ImportStatus.FAILED.value
        assert result.result == result_data
        assert result.result["error"] == "Connection timeout"
        assert result.completed_at is not None
        mock_session.flush.assert_called_once()

    def test_end_job_with_failure_no_result(self, repository, mock_session):
        """Test ending a job with failure and no result data."""
        import_log = ImportLog(
            status=ImportStatus.IN_PROGRESS.value,
            result=None
        )
        import_log.id = 1
        
        result = repository.end_job_with_failure(import_log, None)
        
        assert result.status == ImportStatus.FAILED.value
        assert result.result is None
        mock_session.flush.assert_called_once()

    def test_full_job_lifecycle(self, repository, mock_session):
        """Test a complete job lifecycle: start -> end with success."""
        # Start job
        import_log = repository.start_job(ImportStatus.IN_PROGRESS)
        
        assert import_log.status == ImportStatus.IN_PROGRESS.value
        
        # End job with success
        result_data = {"museums_imported": 100}
        final_log = repository.end_job_with_success(import_log, result_data)
        
        assert final_log.status == ImportStatus.SUCCESS.value
        assert final_log.result == result_data
        assert final_log.completed_at is not None
        assert mock_session.flush.call_count == 2
