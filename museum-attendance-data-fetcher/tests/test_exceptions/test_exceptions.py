"""Tests for exception classes."""
import pytest
from exceptions import (
    MuseumDataFetcherError,
    APIError,
    DataProcessingError,
    DatabaseError,
    ConfigurationError
)


class TestMuseumDataFetcherError:
    """Test suite for MuseumDataFetcherError."""

    def test_create_with_message_only(self):
        """Test creating exception with message only."""
        error = MuseumDataFetcherError("Test error")
        
        assert error.message == "Test error"
        assert error.details == {}
        assert str(error) == "Test error"

    def test_create_with_details(self):
        """Test creating exception with details."""
        details = {"key1": "value1", "key2": "value2"}
        error = MuseumDataFetcherError("Test error", details=details)
        
        assert error.message == "Test error"
        assert error.details == details
        assert "key1=value1" in str(error)
        assert "key2=value2" in str(error)

    def test_str_representation_without_details(self):
        """Test string representation without details."""
        error = MuseumDataFetcherError("Simple error")
        assert str(error) == "Simple error"


class TestAPIError:
    """Test suite for APIError."""

    def test_create_with_status_code(self):
        """Test creating API error with status code."""
        error = APIError("Request failed", status_code=404)
        
        assert error.message == "Request failed"
        assert error.status_code == 404
        assert error.details["status_code"] == 404

    def test_create_with_url(self):
        """Test creating API error with URL."""
        url = "https://api.example.com/test"
        error = APIError("Request failed", url=url)
        
        assert error.url == url
        assert error.details["url"] == url

    def test_create_with_retry_after(self):
        """Test creating API error with retry_after."""
        error = APIError("Rate limited", retry_after=60)
        
        assert error.retry_after == 60
        assert error.details["retry_after"] == 60

    def test_create_with_all_params(self):
        """Test creating API error with all parameters."""
        error = APIError(
            "Full error",
            status_code=429,
            url="https://api.example.com",
            retry_after=120,
            details={"custom": "value"}
        )
        
        assert error.status_code == 429
        assert error.url == "https://api.example.com"
        assert error.retry_after == 120
        assert error.details["custom"] == "value"

    def test_inherits_from_base_exception(self):
        """Test that APIError inherits from MuseumDataFetcherError."""
        error = APIError("Test")
        assert isinstance(error, MuseumDataFetcherError)


class TestDataProcessingError:
    """Test suite for DataProcessingError."""

    def test_create_with_url(self):
        """Test creating error with URL."""
        error = DataProcessingError("Parse error", url="https://example.com")
        
        assert error.url == "https://example.com"
        assert error.details["url"] == "https://example.com"

    def test_create_with_field(self):
        """Test creating error with field."""
        error = DataProcessingError("Invalid field", field="museum_name")
        
        assert error.field == "museum_name"
        assert error.details["field"] == "museum_name"

    def test_create_with_value(self):
        """Test creating error with value."""
        error = DataProcessingError("Invalid value", value="test_value")
        
        assert error.value == "test_value"
        assert error.details["value"] == "test_value"

    def test_create_with_element(self):
        """Test creating error with element."""
        error = DataProcessingError("Element error", element="<div>")
        
        assert error.element == "<div>"
        assert error.details["element"] == "<div>"

    def test_create_with_all_params(self):
        """Test creating error with all parameters."""
        error = DataProcessingError(
            "Complex error",
            url="https://example.com",
            field="name",
            value="test",
            element="<span>",
            details={"extra": "info"}
        )
        
        assert error.url == "https://example.com"
        assert error.field == "name"
        assert error.value == "test"
        assert error.element == "<span>"
        assert error.details["extra"] == "info"

    def test_inherits_from_base_exception(self):
        """Test that DataProcessingError inherits from MuseumDataFetcherError."""
        error = DataProcessingError("Test")
        assert isinstance(error, MuseumDataFetcherError)


class TestDatabaseError:
    """Test suite for DatabaseError."""

    def test_create_with_entity_type(self):
        """Test creating error with entity type."""
        error = DatabaseError("DB error", entity_type="Museum")
        
        assert error.entity_type == "Museum"
        assert error.details["entity_type"] == "Museum"

    def test_create_with_entity_id(self):
        """Test creating error with entity ID."""
        error = DatabaseError("DB error", entity_id="123")
        
        assert error.entity_id == "123"
        assert error.details["entity_id"] == "123"

    def test_create_with_operation(self):
        """Test creating error with operation."""
        error = DatabaseError("DB error", operation="insert")
        
        assert error.operation == "insert"
        assert error.details["operation"] == "insert"

    def test_create_with_all_params(self):
        """Test creating error with all parameters."""
        error = DatabaseError(
            "Complex DB error",
            entity_type="City",
            entity_id="456",
            operation="update",
            details={"constraint": "unique_name"}
        )
        
        assert error.entity_type == "City"
        assert error.entity_id == "456"
        assert error.operation == "update"
        assert error.details["constraint"] == "unique_name"

    def test_inherits_from_base_exception(self):
        """Test that DatabaseError inherits from MuseumDataFetcherError."""
        error = DatabaseError("Test")
        assert isinstance(error, MuseumDataFetcherError)


class TestConfigurationError:
    """Test suite for ConfigurationError."""

    def test_create_with_setting_name(self):
        """Test creating error with setting name."""
        error = ConfigurationError("Invalid setting", setting_name="database_url")
        
        assert error.setting_name == "database_url"
        assert error.details["setting_name"] == "database_url"

    def test_create_with_details(self):
        """Test creating error with custom details."""
        error = ConfigurationError(
            "Config error",
            setting_name="api_key",
            details={"reason": "missing"}
        )
        
        assert error.setting_name == "api_key"
        assert error.details["reason"] == "missing"

    def test_inherits_from_base_exception(self):
        """Test that ConfigurationError inherits from MuseumDataFetcherError."""
        error = ConfigurationError("Test")
        assert isinstance(error, MuseumDataFetcherError)
