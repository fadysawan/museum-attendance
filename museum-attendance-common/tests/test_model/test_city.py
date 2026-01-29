"""Tests for City model."""
import pytest
from museum_attendance_common.model import City


class TestCity:
    """Tests for City model."""

    def test_create_city(self):
        """Test creating a City."""
        city = City(name="Paris", country_id=1, population=2_200_000)
        
        assert city.name == "Paris"
        assert city.population == 2_200_000
        assert city.country_id == 1

    def test_city_without_population(self):
        """Test creating a City without population."""
        city = City(name="Berlin", country_id=2)
        
        assert city.name == "Berlin"
        assert city.country_id == 2
        assert not hasattr(city, 'population') or city.population is None

    def test_city_with_reference_url(self):
        """Test creating a City with reference URL."""
        city = City(
            name="Rome",
            country_id=3,
            reference_url="https://en.wikipedia.org/wiki/Rome"
        )
        
        assert city.reference_url == "https://en.wikipedia.org/wiki/Rome"
        assert city.name == "Rome"

    def test_city_attributes(self):
        """Test City attributes."""
        city = City(name="Madrid", country_id=4, population=3_200_000)
        city.id = 10
        
        assert city.id == 10
        assert city.name == "Madrid"
        assert city.country_id == 4
        assert city.population == 3_200_000
