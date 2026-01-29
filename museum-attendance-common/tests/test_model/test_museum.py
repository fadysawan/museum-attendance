"""Tests for Museum model."""
import pytest
from museum_attendance_common.model import Museum


class TestMuseum:
    """Tests for Museum model."""

    def test_create_museum(self):
        """Test creating a Museum."""
        museum = Museum(
            name="Louvre",
            city_id=1,
            number_of_visitors=9_600_000
        )
        
        assert museum.name == "Louvre"
        assert museum.city_id == 1
        assert museum.number_of_visitors == 9_600_000

    def test_museum_without_visitors(self):
        """Test creating a Museum without visitor count."""
        museum = Museum(name="Prado", city_id=2)
        
        assert museum.name == "Prado"
        assert museum.city_id == 2
        assert not hasattr(museum, 'number_of_visitors') or museum.number_of_visitors is None

    def test_museum_with_reference_url(self):
        """Test creating a Museum with reference URL."""
        museum = Museum(
            name="British Museum",
            city_id=3,
            reference_url="https://en.wikipedia.org/wiki/British_Museum"
        )
        
        assert museum.reference_url == "https://en.wikipedia.org/wiki/British_Museum"
        assert museum.name == "British Museum"

    def test_museum_attributes(self):
        """Test Museum attributes."""
        museum = Museum(name="MET", city_id=4, number_of_visitors=7_000_000)
        museum.id = 100
        
        assert museum.id == 100
        assert museum.name == "MET"
        assert museum.city_id == 4
        assert museum.number_of_visitors == 7_000_000
