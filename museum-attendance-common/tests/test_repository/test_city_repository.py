"""Tests for CityRepository."""
import pytest
from unittest.mock import Mock
from museum_attendance_common.repository import CityRepository
from museum_attendance_common.model import City, Country


class TestCityRepository:
    """Tests for CityRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def repository(self, mock_session):
        """Create a CityRepository with mock session."""
        return CityRepository(mock_session)

    @pytest.fixture
    def mock_country(self):
        """Create a mock Country."""
        country = Country(name="France")
        country.id = 1
        return country

    def test_get_by_name_found(self, repository, mock_session):
        """Test get_by_name when city exists."""
        expected_city = City(name="Paris", country_id=1)
        expected_city.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_city
        
        result = repository.get_by_name("Paris")
        
        assert result == expected_city
        mock_session.query.assert_called_once_with(City)

    def test_get_by_name_not_found(self, repository, mock_session):
        """Test get_by_name when city doesn't exist."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        result = repository.get_by_name("NonExistent")
        
        assert result is None

    def test_persist_city_new(self, repository, mock_session, mock_country):
        """Test persisting a new city."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # City doesn't exist
        
        city, created, updated = repository.persist("London", 8_900_000, "https://example.com", mock_country)
        
        assert isinstance(city, City)
        assert city.name == "London"
        assert city.population == 8_900_000
        assert city.reference_url == "https://example.com"
        assert created is True
        assert updated is False
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    def test_persist_city_existing(self, repository, mock_session, mock_country):
        """Test persisting an existing city (update)."""
        existing_city = City(name="Berlin", country_id=mock_country.id, population=3_500_000)
        existing_city.id = 2
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_city  # City exists
        
        city, created, updated = repository.persist("Berlin", 3_700_000, "https://example.com/berlin", mock_country)
        
        assert city == existing_city
        assert city.population == 3_700_000
        assert city.reference_url == "https://example.com/berlin"
        assert created is False
        assert updated is True
        mock_session.add.assert_not_called()
        mock_session.flush.assert_called_once()

    def test_persist_city_with_none_values(self, repository, mock_session, mock_country):
        """Test persisting city with None values."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        city, created, updated = repository.persist("Rome", None, None, mock_country)
        
        assert city.name == "Rome"
        assert city.population is None
        assert city.reference_url is None
        assert created is True
