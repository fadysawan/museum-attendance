"""Tests for Museum DTO."""
import pytest
from dto import Museum, City
from enumeration import GlobalEnum


class TestMuseum:
    """Test suite for Museum DTO."""

    def test_create_museum(self):
        """Test creating a Museum instance."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={"established": "1793"}
        )
        
        assert museum.name == "Louvre"
        assert museum.visitor_count == 9_600_000

    def test_get_country_from_city_details(self):
        """Test getting country from city details."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="Unknown",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_country() == "France"

    def test_get_country_fallback(self):
        """Test getting country falls back to museum country."""
        city = City(name="Paris", country=GlobalEnum.NA.value, population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_country() == "France"

    def test_get_city_from_city_details(self):
        """Test getting city name from city details."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Unknown",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_city() == "Paris"

    def test_get_city_fallback(self):
        """Test getting city falls back to museum city."""
        city = City(name=GlobalEnum.NA.value, country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_city() == "Paris"

    def test_get_city_population(self):
        """Test getting city population."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_city_population() == 2_165_000

    def test_get_city_reference_url(self):
        """Test getting city reference URL."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_city_reference_url() == "Paris"

    def test_get_museum_attributes(self):
        """Test getting museum attributes."""
        city = City(name="Paris", country="France", population=2_165_000)
        attributes = {"established": "1793", "type": "Art Museum"}
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes=attributes
        )
        
        assert museum.get_museum_attributes() == attributes

    def test_get_museum_reference_url(self):
        """Test getting museum reference URL."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_museum_reference_url() == "Louvre"

    def test_get_museum_name(self):
        """Test getting museum name."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_museum_name() == "Louvre"

    def test_get_museum_visitor_count(self):
        """Test getting museum visitor count."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        
        assert museum.get_museum_visitor_count() == 9_600_000
