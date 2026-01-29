"""Tests for Country model."""
import pytest
from museum_attendance_common.model import Country


class TestCountry:
    """Tests for Country model."""

    def test_create_country(self):
        """Test creating a Country."""
        country = Country(name="France")
        
        assert country.name == "France"
        assert not hasattr(country, 'id') or country.id is None

    def test_country_attributes(self):
        """Test Country attributes."""
        country = Country(name="Germany")
        country.id = 1
        
        assert country.id == 1
        assert country.name == "Germany"

    def test_country_name_assignment(self):
        """Test Country name can be set."""
        country = Country(name="Italy")
        assert country.name == "Italy"
        
        country.name = "Spain"
        assert country.name == "Spain"
