"""Tests for CountryRepository."""
import pytest
from unittest.mock import Mock, MagicMock, call
from museum_attendance_common.repository import CountryRepository
from museum_attendance_common.model import Country
from museum_attendance_common.exceptions import DatabaseError


class TestCountryRepository:
    """Tests for CountryRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def repository(self, mock_session):
        """Create a CountryRepository with mock session."""
        return CountryRepository(mock_session)

    def test_get_by_name_found(self, repository, mock_session):
        """Test get_by_name when country exists."""
        expected_country = Country(name="France")
        expected_country.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_country
        
        result = repository.get_by_name("France")
        
        assert result == expected_country
        mock_session.query.assert_called_once_with(Country)

    def test_get_by_name_not_found(self, repository, mock_session):
        """Test get_by_name when country doesn't exist."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        result = repository.get_by_name("NonExistent")
        
        assert result is None

    def test_add_country_new(self, repository, mock_session):
        """Test adding a new country."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # Country doesn't exist
        
        country, created, updated = repository.add("Germany")
        
        assert isinstance(country, Country)
        assert country.name == "Germany"
        assert created is True
        assert updated is False
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    def test_add_country_existing(self, repository, mock_session):
        """Test adding an existing country."""
        existing_country = Country(name="Italy")
        existing_country.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_country  # Country exists
        
        country, created, updated = repository.add("Italy")
        
        assert country == existing_country
        assert created is False
        assert updated is False
        mock_session.add.assert_not_called()
        mock_session.flush.assert_not_called()
