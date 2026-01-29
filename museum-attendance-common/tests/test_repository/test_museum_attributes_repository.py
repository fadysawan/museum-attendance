"""Tests for MuseumAttributesRepository."""
import pytest
from unittest.mock import Mock
from museum_attendance_common.repository import MuseumAttributesRepository
from museum_attendance_common.model import MuseumAttributes, Museum


class TestMuseumAttributesRepository:
    """Tests for MuseumAttributesRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def repository(self, mock_session):
        """Create a MuseumAttributesRepository with mock session."""
        return MuseumAttributesRepository(mock_session)

    @pytest.fixture
    def mock_museum(self):
        """Create a mock Museum."""
        museum = Museum(name="Louvre", city_id=1)
        museum.id = 1
        return museum

    def test_get_by_museum_and_key_found(self, repository, mock_session, mock_museum):
        """Test get_by_museum_and_key when attribute exists."""
        expected_attr = MuseumAttributes(
            museum_id=1,
            attribute_key="founded",
            attribute_value="1793"
        )
        expected_attr.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = expected_attr
        
        result = repository.get_by_museum_and_key(mock_museum, "founded")
        
        assert result == expected_attr
        mock_session.query.assert_called_once_with(MuseumAttributes)

    def test_get_by_museum_and_key_not_found(self, repository, mock_session, mock_museum):
        """Test get_by_museum_and_key when attribute doesn't exist."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        result = repository.get_by_museum_and_key(mock_museum, "architect")
        
        assert result is None

    def test_persist_attribute_new(self, repository, mock_session, mock_museum):
        """Test persisting a new museum attribute."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # Attribute doesn't exist
        
        attr, created, updated = repository.persist(mock_museum, "director", "John Doe")
        
        assert isinstance(attr, MuseumAttributes)
        assert attr.museum_id == mock_museum.id
        assert attr.attribute_key == "director"
        assert attr.attribute_value == "John Doe"
        assert created is True
        assert updated is False
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()

    def test_persist_attribute_existing(self, repository, mock_session, mock_museum):
        """Test persisting an existing attribute (update)."""
        existing_attr = MuseumAttributes(
            museum_id=mock_museum.id,
            attribute_key="area",
            attribute_value="72735 sq m"
        )
        existing_attr.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_attr  # Attribute exists
        
        attr, created, updated = repository.persist(mock_museum, "area", "80000 sq m")
        
        assert attr == existing_attr
        assert attr.attribute_value == "80000 sq m"
        assert created is False
        assert updated is True
        mock_session.add.assert_not_called()
        mock_session.flush.assert_called_once()

    def test_persist_attribute_with_none_value(self, repository, mock_session, mock_museum):
        """Test persisting attribute with None value."""
        mock_query = Mock()
        mock_filter = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        attr, created, updated = repository.persist(mock_museum, "architect", None)
        
        assert attr.attribute_value is None
        assert created is True
