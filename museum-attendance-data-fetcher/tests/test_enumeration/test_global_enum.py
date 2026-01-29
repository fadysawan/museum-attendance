"""Tests for GlobalEnum."""
import pytest
from enumeration import GlobalEnum


class TestGlobalEnum:
    """Test suite for GlobalEnum."""

    def test_enum_has_na_value(self):
        """Test that GlobalEnum has NA value."""
        assert hasattr(GlobalEnum, 'NA')
        assert GlobalEnum.NA.value == "NA"

    def test_enum_na_comparison(self):
        """Test comparing NA enum value."""
        assert GlobalEnum.NA == GlobalEnum.NA
        assert GlobalEnum.NA.value == "NA"

    def test_enum_string_representation(self):
        """Test string representation of enum."""
        assert str(GlobalEnum.NA.value) == "NA"
