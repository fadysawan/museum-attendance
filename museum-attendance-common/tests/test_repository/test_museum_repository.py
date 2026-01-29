"""Tests for MuseumRepository."""
import pytest
from unittest.mock import Mock
from museum_attendance_common.repository import MuseumRepository
from museum_attendance_common.model import Museum, City


class TestMuseumRepository:
    """Tests for MuseumRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def repository(self, mock_session):
        """Create a MuseumRepository with mock session."""
        return MuseumRepository(mock_session)

    @pytest.fixture
    def mock_city(self):
        """Create a mock City."""
        city = City(name="Paris", country_id=1)
        city.id = 1
        return city

    def test_get_by_name_found(self, repository, mock_session):
        """Test get_by_name when museum exists."""
        expected_museum = Museum(name="Louvre", city_id=1)
        expected_museum.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_museum
        
        result = repository.get_by_name("Louvre")
        
        assert result == expected_museum
        mock_session.query.assert_called_once_with(Museum)

    def test_get_by_name_not_found(self, repository, mock_session):
        """Test get_by_name when museum doesn't exist."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        result = repository.get_by_name("NonExistent")
        
        assert result is None

    def test_persist_museum_new(self, repository, mock_session, mock_city):
        """Test persisting a new museum."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # Museum doesn't exist
        
        museum, created, updated = repository.persist("British Museum", 6_000_000, "https://example.com", mock_city)
        
        assert isinstance(museum, Museum)
        assert museum.name == "British Museum"
        assert museum.number_of_visitors == 6_000_000
        assert museum.reference_url == "https://example.com"
        assert created is True
        assert updated is False
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    def test_persist_museum_existing(self, repository, mock_session, mock_city):
        """Test persisting an existing museum (update)."""
        existing_museum = Museum(name="MET", city_id=mock_city.id, number_of_visitors=6_000_000)
        existing_museum.id = 2
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_museum  # Museum exists
        
        museum, created, updated = repository.persist("MET", 7_000_000, "https://example.com/met", mock_city)
        
        assert museum == existing_museum
        assert museum.number_of_visitors == 7_000_000
        assert created is False
        assert updated is True
        mock_session.add.assert_not_called()
        mock_session.flush.assert_called_once()
