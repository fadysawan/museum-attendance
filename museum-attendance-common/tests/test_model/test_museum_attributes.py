"""Tests for MuseumAttributes model."""
import pytest
from museum_attendance_common.model import MuseumAttributes


class TestMuseumAttributes:
    """Tests for MuseumAttributes model."""

    def test_create_museum_attribute(self):
        """Test creating a MuseumAttribute."""
        attr = MuseumAttributes(
            museum_id=1,
            attribute_key="founded",
            attribute_value="1793"
        )
        
        assert attr.museum_id == 1
        assert attr.attribute_key == "founded"
        assert attr.attribute_value == "1793"

    def test_museum_attribute_with_null_value(self):
        """Test creating a MuseumAttribute with null value."""
        attr = MuseumAttributes(
            museum_id=2,
            attribute_key="architect",
            attribute_value=None
        )
        
        assert attr.museum_id == 2
        assert attr.attribute_key == "architect"
        assert attr.attribute_value is None

    def test_museum_attribute_attributes(self):
        """Test MuseumAttributes attributes."""
        attr = MuseumAttributes(
            museum_id=3,
            attribute_key="director",
            attribute_value="Jane Smith"
        )
        attr.id = 50
        
        assert attr.id == 50
        assert attr.museum_id == 3
        assert attr.attribute_key == "director"
        assert attr.attribute_value == "Jane Smith"

    def test_multiple_attributes_for_same_museum(self):
        """Test creating multiple attributes for the same museum."""
        attrs = [
            MuseumAttributes(museum_id=1, attribute_key="founded", attribute_value="1870"),
            MuseumAttributes(museum_id=1, attribute_key="area", attribute_value="2 million sq ft"),
            MuseumAttributes(museum_id=1, attribute_key="collection_size", attribute_value="2 million"),
        ]
        
        assert len(attrs) == 3
        assert all(attr.museum_id == 1 for attr in attrs)
        keys = [attr.attribute_key for attr in attrs]
        assert "founded" in keys
        assert "area" in keys
        assert "collection_size" in keys
