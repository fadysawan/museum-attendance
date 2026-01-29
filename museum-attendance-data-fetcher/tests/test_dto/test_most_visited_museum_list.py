"""Tests for MostVisitedMuseumList DTO."""
import pytest
from dto import MostVisitedMuseumList, Museum, City


class TestMostVisitedMuseumList:
    """Test suite for MostVisitedMuseumList DTO."""

    def test_create_empty_list(self):
        """Test creating an empty museum list."""
        museum_list = MostVisitedMuseumList(wikipedia_museum_instance_list=[])
        
        assert museum_list.wikipedia_museum_instance_list == []
        assert len(museum_list.wikipedia_museum_instance_list) == 0

    def test_create_list_with_museums(self):
        """Test creating a list with museums."""
        city = City(name="Paris", country="France", population=2_165_000)
        museum1 = Museum(
            name="Louvre",
            visitor_count=9_600_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Louvre",
            wikipedia_museum_attributes={}
        )
        museum2 = Museum(
            name="Musée d'Orsay",
            visitor_count=3_500_000,
            city="Paris",
            wikipedia_city_details_page_title="Paris",
            wikipedia_city_details=city,
            country="France",
            wikipedia_museum_details_page_title="Musée_d'Orsay",
            wikipedia_museum_attributes={}
        )
        
        museum_list = MostVisitedMuseumList(wikipedia_museum_instance_list=[museum1, museum2])
        
        assert len(museum_list.wikipedia_museum_instance_list) == 2
        assert museum_list.wikipedia_museum_instance_list[0].name == "Louvre"
        assert museum_list.wikipedia_museum_instance_list[1].name == "Musée d'Orsay"

    def test_list_iteration(self):
        """Test iterating over museum list."""
        city = City(name="London", country="UK", population=8_982_000)
        museums = [
            Museum(
                name="British Museum",
                visitor_count=6_800_000,
                city="London",
                wikipedia_city_details_page_title="London",
                wikipedia_city_details=city,
                country="UK",
                wikipedia_museum_details_page_title="British_Museum",
                wikipedia_museum_attributes={}
            )
        ]
        
        museum_list = MostVisitedMuseumList(wikipedia_museum_instance_list=museums)
        
        for museum in museum_list.wikipedia_museum_instance_list:
            assert isinstance(museum, Museum)
            assert museum.name == "British Museum"
