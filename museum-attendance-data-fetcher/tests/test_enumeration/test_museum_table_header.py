"""Tests for MuseumTableHeader enumeration."""
import pytest
from enumeration import MuseumTableHeader


class TestMuseumTableHeader:
    """Test suite for MuseumTableHeader enumeration."""

    def test_enum_values(self):
        """Test that all expected enum values exist."""
        assert MuseumTableHeader.NAME.value == "Name"
        assert MuseumTableHeader.VISITORS.value == "Visitors"
        assert MuseumTableHeader.CITY.value == "City"
        assert MuseumTableHeader.COUNTRY.value == "Country"

    def test_enum_members(self):
        """Test that enum has all expected members."""
        expected_members = {"NAME", "VISITORS", "CITY", "COUNTRY"}
        actual_members = {member.name for member in MuseumTableHeader}
        assert actual_members == expected_members

    def test_enum_comparison(self):
        """Test enum comparison."""
        assert MuseumTableHeader.NAME == MuseumTableHeader.NAME
        assert MuseumTableHeader.NAME != MuseumTableHeader.VISITORS

    def test_enum_from_value(self):
        """Test getting enum from value."""
        assert MuseumTableHeader("Name") == MuseumTableHeader.NAME
        assert MuseumTableHeader("Visitors") == MuseumTableHeader.VISITORS

    def test_enum_string_representation(self):
        """Test string representation of enum."""
        assert str(MuseumTableHeader.NAME.value) == "Name"
        assert str(MuseumTableHeader.CITY.value) == "City"
