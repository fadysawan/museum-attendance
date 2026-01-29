"""Tests for exception classes."""
import pytest
from museum_attendance_common.exceptions import MuseumDataFetcherError, DatabaseError


class TestMuseumDataFetcherError:
    """Tests for MuseumDataFetcherError base exception."""

    def test_create_with_message_only(self):
        """Test creating exception with message only."""
        error = MuseumDataFetcherError("Test error message")
        
        assert error.message == "Test error message"
        assert error.details == {}
        assert str(error) == "Test error message"

    def test_create_with_details(self):
        """Test creating exception with details."""
        details = {"key1": "value1", "key2": "value2"}
        error = MuseumDataFetcherError("Test error", details=details)
        
        assert error.message == "Test error"
        assert error.details == details
        assert "key1=value1" in str(error)
        assert "key2=value2" in str(error)

    def test_create_with_none_details(self):
        """Test creating exception with None details."""
        error = MuseumDataFetcherError("Test error", details=None)
        
        assert error.message == "Test error"
        assert error.details == {}

    def test_str_representation_without_details(self):
        """Test string representation without details."""
        error = MuseumDataFetcherError("Error message")
        
        assert str(error) == "Error message"

    def test_str_representation_with_details(self):
        """Test string representation with details."""
        error = MuseumDataFetcherError("Error message", details={"code": 500, "source": "api"})
        
        error_str = str(error)
        assert "Error message" in error_str
        assert "code=500" in error_str
        assert "source=api" in error_str


class TestDatabaseError:
    """Tests for DatabaseError exception."""

    def test_create_with_message_only(self):
        """Test creating DatabaseError with message only."""
        error = DatabaseError("Database connection failed")
        
        assert error.message == "Database connection failed"
        assert error.entity_type is None
        assert error.entity_id is None
        assert error.operation is None
        assert error.details == {}

    def test_create_with_entity_info(self):
        """Test creating DatabaseError with entity information."""
        error = DatabaseError(
            "Failed to save entity",
            entity_type="Museum",
            entity_id="123",
            operation="insert"
        )
        
        assert error.message == "Failed to save entity"
        assert error.entity_type == "Museum"
        assert error.entity_id == "123"
        assert error.operation == "insert"
        assert "entity_type" in error.details
        assert error.details["entity_type"] == "Museum"
        assert error.details["entity_id"] == "123"
        assert error.details["operation"] == "insert"

    def test_create_with_custom_details(self):
        """Test creating DatabaseError with custom details."""
        custom_details = {"constraint": "unique_name", "table": "museums"}
        error = DatabaseError(
            "Unique constraint violation",
            entity_type="Museum",
            details=custom_details
        )
        
        assert error.details["entity_type"] == "Museum"
        assert error.details["constraint"] == "unique_name"
        assert error.details["table"] == "museums"

    def test_inherits_from_base_exception(self):
        """Test that DatabaseError inherits from MuseumDataFetcherError."""
        error = DatabaseError("Test error")
        
        assert isinstance(error, MuseumDataFetcherError)
        assert isinstance(error, Exception)

    def test_str_representation_with_entity_info(self):
        """Test string representation includes entity info."""
        error = DatabaseError(
            "Failed to update",
            entity_type="City",
            entity_id="456",
            operation="update"
        )
        
        error_str = str(error)
        assert "Failed to update" in error_str
        assert "entity_type=City" in error_str
        assert "entity_id=456" in error_str
        assert "operation=update" in error_str

    def test_none_values_not_added_to_details(self):
        """Test that None values are not added to details."""
        error = DatabaseError("Test error", entity_type="Museum", entity_id=None)
        
        assert "entity_type" in error.details
        assert "entity_id" not in error.details
