"""Tests for DataCollectionService."""
import pytest
from unittest.mock import Mock, MagicMock, patch
from bs4 import BeautifulSoup

from service.data_collection_service import DataCollectionService
from dto import Museum, City, MostVisitedMuseumList


class TestDataCollectionService:
    """Test suite for DataCollectionService."""

    @pytest.fixture
    def sample_museum(self):
        """Create a sample Museum DTO."""
        return Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=City(name="Paris", country="France", population=0),
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )

    @pytest.fixture
    def sample_museums_list(self, sample_museum):
        """Create a sample list of museums."""
        return [sample_museum]

    @patch('service.data_collection_service.wikipedia_service')
    @patch('service.data_collection_service.MuseumListPageExtractor')
    @patch('service.data_collection_service.ThreadPoolExecutor')
    def test_collect_data_success(self, mock_executor, mock_extractor_class, mock_wiki_service, sample_museums_list):
        """Test successful data collection."""
        # Mock Wikipedia service
        mock_wiki_service.get_page_html.return_value = "<html>Museum list content</html>"
        
        # Mock extractor
        mock_extractor = Mock()
        mock_extractor.to_dto.return_value = sample_museums_list
        mock_extractor_class.return_value = mock_extractor
        
        # Mock ThreadPoolExecutor
        mock_executor_instance = MagicMock()
        mock_executor.return_value.__enter__.return_value = mock_executor_instance
        
        # Mock futures
        mock_future = Mock()
        mock_future.result.return_value = sample_museums_list[0]
        mock_executor_instance.submit.return_value = mock_future
        
        with patch('service.data_collection_service.as_completed') as mock_as_completed:
            mock_as_completed.side_effect = [[mock_future], [mock_future]]
            
            result = DataCollectionService.collect_data("List_of_most_visited_museums")
        
        assert isinstance(result, MostVisitedMuseumList)
        assert len(result.wikipedia_museum_instance_list) == 1
        mock_wiki_service.get_page_html.assert_called_once_with("List_of_most_visited_museums")

    @patch('service.data_collection_service.wikipedia_service')
    @patch('service.data_collection_service.MuseumInstancePageExtractor')
    def test_fetch_museum_details_success(self, mock_extractor_class, mock_wiki_service, sample_museum):
        """Test successful museum details fetching."""
        mock_wiki_service.get_page_html.return_value = "<html>Museum details</html>"
        
        mock_extractor = Mock()
        mock_extractor.extract_data.return_value = {"established": "1793"}
        mock_extractor_class.return_value = mock_extractor
        
        result = DataCollectionService.fetch_museum_details(sample_museum)
        
        assert result.wikipedia_museum_attributes == {"established": "1793"}
        mock_wiki_service.get_page_html.assert_called_once_with("Louvre")

    @patch('service.data_collection_service.wikipedia_service')
    def test_fetch_museum_details_handles_error(self, mock_wiki_service, sample_museum):
        """Test that fetch_museum_details handles errors gracefully."""
        mock_wiki_service.get_page_html.side_effect = Exception("Network error")
        
        result = DataCollectionService.fetch_museum_details(sample_museum)
        
        # Should return original museum without crashing
        assert result.name == "Louvre"
        assert result.wikipedia_museum_attributes == {}

    @patch('service.data_collection_service.wikipedia_service')
    @patch('service.data_collection_service.CityPageExtractor')
    def test_fetch_city_details_success(self, mock_extractor_class, mock_wiki_service, sample_museum):
        """Test successful city details fetching."""
        mock_wiki_service.get_page_html.return_value = "<html>City details</html>"
        
        city_dto = City(name="Paris", country="France", population=2_165_000)
        mock_extractor = Mock()
        mock_extractor.to_dto.return_value = city_dto
        mock_extractor_class.return_value = mock_extractor
        
        result = DataCollectionService.fetch_city_details(sample_museum)
        
        assert result.wikipedia_city_details.name == "Paris"
        assert result.wikipedia_city_details.population == 2_165_000
        mock_wiki_service.get_page_html.assert_called_once_with("Paris")

    @patch('service.data_collection_service.wikipedia_service')
    def test_fetch_city_details_handles_error(self, mock_wiki_service, sample_museum):
        """Test that fetch_city_details handles errors gracefully."""
        mock_wiki_service.get_page_html.side_effect = Exception("Network error")
        
        result = DataCollectionService.fetch_city_details(sample_museum)
        
        # Should return original museum without crashing
        assert result.name == "Louvre"
        assert result.city == "Paris"
