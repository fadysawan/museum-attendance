"""Tests for PersistenceService."""
import pytest
from unittest.mock import Mock, MagicMock

from service.persistence_service import PersistenceService
from museum_attendance_common.model import Country, City, Museum
from museum_attendance_common.exceptions import DatabaseError
from dto import Museum as MuseumDTO, City as CityDTO
from exceptions import DataProcessingError


class TestPersistenceService:
    """Test suite for PersistenceService."""

    @pytest.fixture
    def mock_repositories(self):
        """Create mock repositories."""
        return {
            'museum_repository': Mock(),
            'country_repository': Mock(),
            'museum_attributes_repository': Mock(),
            'city_repository': Mock()
        }

    @pytest.fixture
    def persistence_service(self, mock_repositories):
        """Create a PersistenceService instance with mocked repositories."""
        return PersistenceService(**mock_repositories)

    @pytest.fixture
    def sample_country(self):
        """Create a sample Country model."""
        country = Country()
        country.id = 1
        country.name = "France"
        return country

    @pytest.fixture
    def sample_city(self, sample_country):
        """Create a sample City model."""
        city = City()
        city.id = 1
        city.name = "Paris"
        city.population = 2_165_000
        city.country_id = sample_country.id
        return city

    @pytest.fixture
    def sample_museum_dto(self):
        """Create a sample Museum DTO."""
        city_dto = CityDTO(name="Paris", country="France", population=2_165_000)
        return MuseumDTO(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city_dto,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={"established": "1793", "type": "Art Museum"}
        )

    def test_persist_country_success(self, persistence_service, sample_country, mock_repositories):
        """Test successful country persistence."""
        mock_repositories['country_repository'].add.return_value = (sample_country, True, False)
        
        country, inserted, updated = persistence_service.persist_country("France")
        
        assert country == sample_country
        assert inserted is True
        assert updated is False
        mock_repositories['country_repository'].add.assert_called_once_with("France")

    def test_persist_country_empty_name(self, persistence_service):
        """Test persisting country with empty name raises error."""
        with pytest.raises(DataProcessingError) as exc_info:
            persistence_service.persist_country("")
        
        assert "Country name cannot be empty" in str(exc_info.value)

    def test_persist_country_database_error(self, persistence_service, mock_repositories):
        """Test handling database error when persisting country."""
        mock_repositories['country_repository'].add.side_effect = DatabaseError("DB connection lost")
        
        with pytest.raises(DatabaseError):
            persistence_service.persist_country("France")

    def test_persist_country_unexpected_error(self, persistence_service, mock_repositories):
        """Test handling unexpected error when persisting country."""
        mock_repositories['country_repository'].add.side_effect = Exception("Unexpected error")
        
        with pytest.raises(DataProcessingError) as exc_info:
            persistence_service.persist_country("France")
        
        assert "Failed to persist country" in str(exc_info.value)

    def test_persist_city_success(self, persistence_service, sample_museum_dto, sample_country, sample_city, mock_repositories):
        """Test successful city persistence."""
        mock_repositories['city_repository'].persist.return_value = (sample_city, True, False)
        
        city, inserted, updated = persistence_service.persist_city(sample_museum_dto, sample_country)
        
        assert city == sample_city
        assert inserted is True
        assert updated is False
        mock_repositories['city_repository'].persist.assert_called_once_with(
            "Paris", 2_165_000, "Paris", sample_country
        )

    def test_persist_city_empty_name(self, persistence_service, sample_country):
        """Test persisting city with empty name raises error."""
        city_dto = CityDTO(name="", country="France", population=0)
        museum_dto = MuseumDTO(
            name="Test Museum",
            visitor_count=1000,
            city="",
            wikipedia_city_details_page_title="",
            wikipedia_city_details=city_dto,
            country="France",
            wikipedia_museum_details_page_title="Test",
            wikipedia_museum_attributes={}
        )
        
        with pytest.raises(DataProcessingError) as exc_info:
            persistence_service.persist_city(museum_dto, sample_country)
        
        assert "City name cannot be empty" in str(exc_info.value)

    def test_persist_city_database_error(self, persistence_service, sample_museum_dto, sample_country, mock_repositories):
        """Test handling database error when persisting city."""
        mock_repositories['city_repository'].persist.side_effect = DatabaseError("DB error")
        
        with pytest.raises(DatabaseError):
            persistence_service.persist_city(sample_museum_dto, sample_country)

    def test_persist_city_unexpected_error(self, persistence_service, sample_museum_dto, sample_country, mock_repositories):
        """Test handling unexpected error when persisting city."""
        mock_repositories['city_repository'].persist.side_effect = Exception("Unexpected error")
        
        with pytest.raises(DataProcessingError) as exc_info:
            persistence_service.persist_city(sample_museum_dto, sample_country)
        
        assert "Failed to persist city" in str(exc_info.value)

    def test_persist_museum_success(self, persistence_service, sample_museum_dto, sample_city, mock_repositories):
        """Test successful museum persistence."""
        museum = Museum()
        museum.id = 1
        museum.name = "Louvre"
        mock_repositories['museum_repository'].persist.return_value = (museum, True, False)
        
        result_museum, inserted, updated = persistence_service.persist_museum(sample_museum_dto, sample_city)
        
        assert result_museum == museum
        assert inserted is True
        assert updated is False
        mock_repositories['museum_repository'].persist.assert_called_once_with(
            name="Louvre",
            number_of_visitors=9_600_000,
            reference_url="Louvre",
            city=sample_city
        )

    def test_persist_museum_empty_name(self, persistence_service, sample_city):
        """Test persisting museum with empty name raises error."""
        city_dto = CityDTO(name="Paris", country="France", population=2_165_000)
        museum_dto = MuseumDTO(
            name="",
            visitor_count=1000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city_dto,
            country="France",
            wikipedia_museum_details_page_title="Test",
            wikipedia_museum_attributes={}
        )
        
        with pytest.raises(DataProcessingError) as exc_info:
            persistence_service.persist_museum(museum_dto, sample_city)
        
        assert "Museum name cannot be empty" in str(exc_info.value)

    def test_persist_museum_database_error(self, persistence_service, sample_museum_dto, sample_city, mock_repositories):
        """Test handling database error when persisting museum."""
        mock_repositories['museum_repository'].persist.side_effect = DatabaseError("DB error")
        
        with pytest.raises(DatabaseError):
            persistence_service.persist_museum(sample_museum_dto, sample_city)

    def test_persist_museum_unexpected_error(self, persistence_service, sample_museum_dto, sample_city, mock_repositories):
        """Test handling unexpected error when persisting museum."""
        mock_repositories['museum_repository'].persist.side_effect = Exception("Unexpected error")
        
        with pytest.raises(DataProcessingError) as exc_info:
            persistence_service.persist_museum(sample_museum_dto, sample_city)
        
        assert "Failed to persist museum" in str(exc_info.value)

    def test_persist_museum_attributes_success(self, persistence_service, mock_repositories):
        """Test successful museum attributes persistence."""
        museum = Museum()
        museum.id = 1
        attributes = {"established": "1793", "type": "Art Museum", "architect": "Unknown"}
        
        # Mock each attribute persistence
        mock_repositories['museum_attributes_repository'].persist.side_effect = [
            (Mock(), True, False),   # First attribute inserted
            (Mock(), False, True),   # Second attribute updated
            (Mock(), True, False),   # Third attribute inserted
        ]
        
        inserted_count, updated_count = persistence_service.persist_museum_attributes(attributes, museum)
        
        assert inserted_count == 2
        assert updated_count == 1
        assert mock_repositories['museum_attributes_repository'].persist.call_count == 3

    def test_persist_museum_attributes_empty_dict(self, persistence_service, mock_repositories):
        """Test persisting empty museum attributes dictionary."""
        museum = Museum()
        museum.id = 1
        
        inserted_count, updated_count = persistence_service.persist_museum_attributes({}, museum)
        
        assert inserted_count == 0
        assert updated_count == 0
        mock_repositories['museum_attributes_repository'].persist.assert_not_called()

    def test_persist_museum_attributes_database_error(self, persistence_service, mock_repositories):
        """Test handling database error when persisting museum attributes."""
        museum = Museum()
        museum.id = 1
        attributes = {"established": "1793"}
        
        mock_repositories['museum_attributes_repository'].persist.side_effect = DatabaseError("DB error")
        
        with pytest.raises(DatabaseError):
            persistence_service.persist_museum_attributes(attributes, museum)
