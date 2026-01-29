"""Tests for ImportStatus enumeration."""
from museum_attendance_common.enumeration import ImportStatus


class TestImportStatus:
    """Tests for ImportStatus enum."""

    def test_enum_values(self):
        """Test that enum has correct values."""
        assert ImportStatus.IN_PROGRESS.value == "IN_PROGRESS"
        assert ImportStatus.FAILED.value == "FAILED"
        assert ImportStatus.SUCCESS.value == "SUCCESS"

    def test_enum_members(self):
        """Test that enum has correct members."""
        members = [member.name for member in ImportStatus]
        assert "IN_PROGRESS" in members
        assert "FAILED" in members
        assert "SUCCESS" in members
        assert len(members) == 3

    def test_enum_comparison(self):
        """Test enum member comparison."""
        status1 = ImportStatus.IN_PROGRESS
        status2 = ImportStatus.IN_PROGRESS
        status3 = ImportStatus.SUCCESS
        
        assert status1 == status2
        assert status1 != status3
        assert status1 is status2

    def test_enum_from_value(self):
        """Test creating enum from value."""
        status = ImportStatus("IN_PROGRESS")
        assert status == ImportStatus.IN_PROGRESS
        
        status = ImportStatus("FAILED")
        assert status == ImportStatus.FAILED
        
        status = ImportStatus("SUCCESS")
        assert status == ImportStatus.SUCCESS

    def test_enum_string_representation(self):
        """Test string representation of enum."""
        assert str(ImportStatus.IN_PROGRESS) == "ImportStatus.IN_PROGRESS"
        assert str(ImportStatus.FAILED) == "ImportStatus.FAILED"
        assert str(ImportStatus.SUCCESS) == "ImportStatus.SUCCESS"

    def test_enum_name_and_value_access(self):
        """Test accessing name and value properties."""
        status = ImportStatus.IN_PROGRESS
        assert status.name == "IN_PROGRESS"
        assert status.value == "IN_PROGRESS"
