"""Tests for database configuration."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from museum_attendance_common.config.database import get_engine, get_db_session, close_db
from museum_attendance_common.exceptions import DatabaseError


class TestGetEngine:
    """Tests for get_engine function."""

    @patch('museum_attendance_common.config.database.create_engine')
    @patch('museum_attendance_common.config.database.Settings')
    def test_get_engine_creates_engine(self, mock_settings_class, mock_create_engine):
        """Test that get_engine creates an engine successfully."""
        mock_settings = Mock()
        mock_settings.database_url = "postgresql://user:pass@localhost/testdb"
        mock_settings.db_pool_size = 5
        mock_settings.db_max_overflow = 10
        mock_settings.db_pool_timeout = 30
        mock_settings.db_pool_recycle = 3600
        mock_settings_class.return_value = mock_settings
        
        mock_engine = Mock(spec=Engine)
        mock_create_engine.return_value = mock_engine
        
        # Mock connection test with MagicMock for context manager
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        
        engine = get_engine()
        
        assert engine == mock_engine
        mock_create_engine.assert_called_once()

    @patch('museum_attendance_common.config.database.create_engine')
    @patch('museum_attendance_common.config.database.Settings')
    def test_get_engine_returns_cached_instance(self, mock_settings_class, mock_create_engine):
        """Test that get_engine returns the same cached engine instance."""
        mock_settings = Mock()
        mock_settings.database_url = "postgresql://user:pass@localhost/testdb"
        mock_settings.db_pool_size = 5
        mock_settings.db_max_overflow = 10
        mock_settings.db_pool_timeout = 30
        mock_settings.db_pool_recycle = 3600
        mock_settings_class.return_value = mock_settings
        
        mock_engine = Mock(spec=Engine)
        mock_create_engine.return_value = mock_engine
        
        # Mock connection test with MagicMock for context manager
        mock_conn = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_conn = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Reset the global engine for this test
        import museum_attendance_common.config.database as db_module
        db_module._engine = None
        db_module._SessionLocal = None
        
        engine1 = get_engine()
        engine2 = get_engine()
        
        assert engine1 is engine2
        # Should only create engine once
        assert mock_create_engine.call_count == 1

    @patch('museum_attendance_common.config.database.create_engine')
    @patch('museum_attendance_common.config.database.Settings')
    def test_get_engine_handles_connection_error(self, mock_settings_class, mock_create_engine):
        """Test that get_engine handles connection errors."""
        mock_settings = Mock()
        mock_settings.database_url = "postgresql://user:pass@localhost/testdb"
        mock_settings.db_pool_size = 5
        mock_settings.db_max_overflow = 10
        mock_settings.db_pool_timeout = 30
        mock_settings.db_pool_recycle = 3600
        mock_settings_class.return_value = mock_settings
        
        mock_engine = Mock(spec=Engine)
        mock_create_engine.return_value = mock_engine
        
        # Mock connection failure
        mock_engine.connect.side_effect = OperationalError("Connection failed", None, None)
        
        # Reset the global engine for this test
        import museum_attendance_common.config.database as db_module
        db_module._engine = None
        db_module._SessionLocal = None
        
        with pytest.raises(DatabaseError) as exc_info:
            get_engine()
        
        assert "Cannot connect to database" in str(exc_info.value)
    """Tests for get_db_session function."""

    @patch('museum_attendance_common.config.database.get_engine')
    def test_get_db_session_yields_session(self, mock_get_engine):
        """Test that get_db_session yields a session."""
        mock_engine = Mock(spec=Engine)
        mock_get_engine.return_value = mock_engine
        
        mock_session = MagicMock(spec=Session)
        # Mock the session state collections
        mock_session.new = []
        mock_session.dirty = []
        mock_session.deleted = []
        
        with patch('museum_attendance_common.config.database._SessionLocal') as mock_session_local:
            mock_session_local.return_value = mock_session
            
            # Reset global variables
            import museum_attendance_common.config.database as db_module
            db_module._SessionLocal = mock_session_local
            
            with get_db_session() as session:
                assert session == mock_session
            
            mock_session.commit.assert_called_once()

    @patch('museum_attendance_common.config.database.get_engine')
    def test_get_db_session_rolls_back_on_error(self, mock_get_engine):
        """Test that get_db_session rolls back on error."""
        mock_engine = Mock(spec=Engine)
        mock_get_engine.return_value = mock_engine
        
        mock_session = MagicMock(spec=Session)
        # Mock the session state collections
        mock_session.new = []
        mock_session.dirty = []
        mock_session.deleted = []
        
        with patch('museum_attendance_common.config.database._SessionLocal') as mock_session_local:
            mock_session_local.return_value = mock_session
            
            # Reset global variables
            import museum_attendance_common.config.database as db_module
            db_module._SessionLocal = mock_session_local
            
            with pytest.raises(DatabaseError):
                with get_db_session() as session:
                    raise ValueError("Test error")
            
            mock_session.rollback.assert_called_once()


class TestCloseDb:
    """Tests for close_db function."""

    @patch('museum_attendance_common.config.database._engine')
    def test_close_db_disposes_engine(self, mock_engine):
        """Test that close_db disposes the engine."""
        mock_engine_instance = Mock(spec=Engine)
        mock_engine = mock_engine_instance
        
        # Mock pool stats
        mock_pool = Mock()
        mock_pool.size.return_value = 5
        mock_pool.checkedin.return_value = 3
        mock_engine_instance.pool = mock_pool
        
        import museum_attendance_common.config.database as db_module
        db_module._engine = mock_engine_instance
        
        close_db()
        
        mock_engine_instance.dispose.assert_called_once()

    def test_close_db_handles_none_engine(self):
        """Test that close_db handles None engine gracefully."""
        import museum_attendance_common.config.database as db_module
        db_module._engine = None
        
        # Should not raise an exception
        close_db()


class TestInit:
    """Init file for test_config package."""
    pass
