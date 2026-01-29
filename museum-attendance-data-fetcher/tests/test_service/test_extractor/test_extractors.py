"""Tests for extractor classes."""
import pytest
from bs4 import BeautifulSoup
from unittest.mock import Mock, patch

from service.extractor import CityPageExtractor, MuseumInstancePageExtractor, MuseumListPageExtractor
from dto import City, Museum
from exceptions import DataProcessingError


class TestCityPageExtractor:
    """Test suite for CityPageExtractor."""

    def test_parse_html(self):
        """Test HTML parsing."""
        html = "<html><body><h1>Paris</h1></body></html>"
        extractor = CityPageExtractor(_html_content=html)
        
        soup = extractor.parse_html()
        assert isinstance(soup, BeautifulSoup)
        assert soup.find('h1').text == "Paris"

    def test_get_html_content(self):
        """Test getting HTML content."""
        html = "<html><body>Test</body></html>"
        extractor = CityPageExtractor(_html_content=html)
        
        assert extractor.get_html_content() == html

    @patch('service.extractor.city_page_extractor.parser')
    def test_extract_data_with_population(self, mock_parser):
        """Test extracting city data with population."""
        html = '''
        <html>
            <body>
                <table class="infobox">
                    <tr><th>Country</th><td>France</td></tr>
                    <tr><th>Population</th><td>2,165,423</td></tr>
                </table>
            </body>
        </html>
        '''
        
        mock_quantity = Mock()
        mock_quantity.value = 2165423
        mock_parser.parse.return_value = [mock_quantity]
        
        extractor = CityPageExtractor(_html_content=html)
        soup = extractor.parse_html()
        data = extractor.extract_data(soup)
        
        assert 'name' in data
        assert data['country'] == "France"
        assert data['population'] == 2165423

    def test_to_dto(self):
        """Test converting to DTO."""
        html = '''
        <html>
            <body>
                <h1>Paris</h1>
                <table class="infobox">
                    <tr><th>Country</th><td>France</td></tr>
                </table>
            </body>
        </html>
        '''
        
        extractor = CityPageExtractor(_html_content=html)
        
        with patch.object(extractor, 'extract_data') as mock_extract:
            mock_extract.return_value = {
                'name': 'Paris',
                'country': 'France',
                'population': 2165423
            }
            
            city = extractor.to_dto()
            
            assert isinstance(city, City)
            assert city.name == 'Paris'
            assert city.country == 'France'
            assert city.population == 2165423


class TestMuseumInstancePageExtractor:
    """Test suite for MuseumInstancePageExtractor."""

    def test_parse_html(self):
        """Test HTML parsing."""
        html = "<html><body><h1>Louvre</h1></body></html>"
        extractor = MuseumInstancePageExtractor(_html_content=html)
        
        soup = extractor.parse_html()
        assert isinstance(soup, BeautifulSoup)

    def test_extract_data_with_infobox(self):
        """Test extracting museum attributes from infobox."""
        html = '''
        <html>
            <body>
                <table class="infobox">
                    <tr><th>Established</th><td>1793</td></tr>
                    <tr><th>Type</th><td>Art museum</td></tr>
                    <tr><th>Director</th><td>Laurence des Cars</td></tr>
                </table>
            </body>
        </html>
        '''
        
        extractor = MuseumInstancePageExtractor(_html_content=html)
        soup = extractor.parse_html()
        data = extractor.extract_data(soup)
        
        assert isinstance(data, dict)
        assert 'established' in data  # Keys are lowercased and underscored
        assert data['established'] == '1793'
        assert data['type'] == 'Art museum'

    def test_extract_data_empty_infobox(self):
        """Test extracting from page with no infobox."""
        html = "<html><body><h1>Museum</h1></body></html>"
        
        extractor = MuseumInstancePageExtractor(_html_content=html)
        soup = extractor.parse_html()
        data = extractor.extract_data(soup)
        
        assert isinstance(data, dict)
        assert len(data) == 0

    def test_to_dto_returns_dict(self):
        """Test that to_dto returns extracted data dict."""
        html = "<html><body><table class='infobox'><tr><th>Test</th><td>Value</td></tr></table></body></html>"
        extractor = MuseumInstancePageExtractor(_html_content=html)
        
        data = extractor.to_dto()
        
        assert isinstance(data, dict)
        assert 'test' in data


class TestMuseumListPageExtractor:
    """Test suite for MuseumListPageExtractor."""

    def test_parse_html(self):
        """Test HTML parsing."""
        html = "<html><body><h1>Museums</h1></body></html>"
        extractor = MuseumListPageExtractor(_html_content=html)
        
        soup = extractor.parse_html()
        assert isinstance(soup, BeautifulSoup)

    @patch('service.extractor.museum_list_page_extractor.parser')
    def test_extract_data_with_table(self, mock_parser):
        """Test extracting museum list from Wikipedia table."""
        html = '''
        <html>
            <body>
                <table class="wikitable sortable">
                    <tbody>
                        <tr>
                            <th>Name</th>
                            <th>City</th>
                            <th>Country</th>
                            <th>Visitors</th>
                        </tr>
                        <tr>
                            <td><a href="/wiki/Louvre">Louvre</a></td>
                            <td><a href="/wiki/Paris">Paris</a></td>
                            <td>France</td>
                            <td>9,600,000</td>
                        </tr>
                    </tbody>
                </table>
            </body>
        </html>
        '''
        
        mock_quantity = Mock()
        mock_quantity.value = 9600000
        mock_parser.parse.return_value = [mock_quantity]
        
        extractor = MuseumListPageExtractor(_html_content=html)
        soup = extractor.parse_html()
        data = extractor.extract_data(soup)
        
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_to_dto(self):
        """Test converting to DTO list."""
        html = "<html><body><table class='wikitable'></table></body></html>"
        
        extractor = MuseumListPageExtractor(_html_content=html)
        
        with patch.object(extractor, 'get_data') as mock_get_data:
            # Return a dict with numeric keys (as the extractor actually returns)
            mock_get_data.return_value = {
                0: {
                    'name': 'Louvre',
                    'city': 'Paris',
                    'country': 'France',
                    'visitor_count': 9600000,
                    'wikipedia_city_details_page_title': 'Paris',
                    'wikipedia_museum_details_page_title': 'Louvre',
                    'wikipedia_city_details': None,
                    'wikipedia_museum_attributes': None
                }
            }
            
            museums = extractor.to_dto()
            
            assert isinstance(museums, list)
            assert len(museums) == 1
            assert isinstance(museums[0], Museum)
            assert museums[0].name == 'Louvre'


class TestAbstractWikipediaPageExtractor:
    """Test suite for AbstractWikipediaPageExtractor base functionality."""

    def test_get_data(self):
        """Test get_data method."""
        html = '''
        <html>
            <body>
                <table class="infobox">
                    <tr><th>Test</th><td>Value</td></tr>
                </table>
            </body>
        </html>
        '''
        
        extractor = MuseumInstancePageExtractor(_html_content=html)
        data = extractor.get_data()
        
        assert isinstance(data, dict)
