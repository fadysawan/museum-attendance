"""Tests for City DTO."""
import pytest
from dto import City


class TestCity:
    """Test suite for City DTO."""

    def test_create_city(self):
        """Test creating a City instance."""
        city = City(name="Paris", country="France", population=2_165_000)
        
        assert city.name == "Paris"
        assert city.country == "France"
        assert city.population == 2_165_000

    def test_city_with_large_population(self):
        """Test city with large population."""
        city = City(name="Tokyo", country="Japan", population=13_960_000)
        
        assert city.population == 13_960_000

    def test_city_equality(self):
        """Test that two cities with same values are equal."""
        city1 = City(name="London", country="UK", population=8_982_000)
        city2 = City(name="London", country="UK", population=8_982_000)
        
        assert city1 == city2

    def test_city_attributes(self):
        """Test that City has all required attributes."""
        city = City(name="Berlin", country="Germany", population=3_769_000)
        
        assert hasattr(city, 'name')
        assert hasattr(city, 'country')
        assert hasattr(city, 'population')
