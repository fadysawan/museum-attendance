"""Tests for Settings configuration."""
import os
from pathlib import Path
from museum_attendance_common.config.settings import Settings


class TestSettings:
    """Tests for Settings class."""

    def test_settings_default_values(self):
        """Test Settings with default values."""
        settings = Settings(
            wikipedia_client_id="test_id",
            wikipedia_client_secret="test_secret"
        )
        
        assert settings.db_user == "IL_USER"
        assert settings.db_password == "postgres"
        assert settings.db_host == "localhost"
        assert settings.db_port == 5432
        assert settings.db_name == "museum_attendance"
        assert settings.db_pool_size == 1
        assert settings.db_max_overflow == 0
        assert settings.db_pool_timeout == 30
        assert settings.db_pool_recycle == 3600
        assert settings.keep_html_files is False
        assert settings.rate_limit_calls == 2
        assert settings.rate_limit_period == 1
        assert settings.max_workers == 5
        assert settings.log_level == "INFO"

    def test_settings_custom_values(self):
        """Test Settings with custom values."""
        settings = Settings(
            db_user="custom_user",
            db_password="custom_pass",
            db_host="custom_host",
            db_port=5433,
            db_name="custom_db",
            db_pool_size=5,
            db_max_overflow=10,
            keep_html_files=True,
            rate_limit_calls=5,
            rate_limit_period=2,
            max_workers=10,
            log_level="DEBUG",
            wikipedia_client_id="test_id",
            wikipedia_client_secret="test_secret",
        )
        
        assert settings.db_user == "custom_user"
        assert settings.db_password == "custom_pass"
        assert settings.db_host == "custom_host"
        assert settings.db_port == 5433
        assert settings.db_name == "custom_db"
        assert settings.db_pool_size == 5
        assert settings.db_max_overflow == 10
        assert settings.keep_html_files is True
        assert settings.rate_limit_calls == 5
        assert settings.rate_limit_period == 2
        assert settings.max_workers == 10
        assert settings.log_level == "DEBUG"

    def test_database_url_property(self):
        """Test database_url property."""
        settings = Settings(
            db_user="test_user",
            db_password="test_pass",
            db_host="test_host",
            db_port=5432,
            db_name="test_db",
            wikipedia_client_id="test_id",
            wikipedia_client_secret="test_secret",
        )
        
        url = str(settings.database_url)  # Convert to string
        assert "postgresql+psycopg2://" in url
        assert "test_user" in url
        assert "test_host" in url
        assert "5432" in url
        assert "test_db" in url

    def test_wikipedia_credentials(self):
        """Test Wikipedia API credentials."""
        settings = Settings(
            wikipedia_client_id="my_client_id",
            wikipedia_client_secret="my_client_secret",
        )
        
        assert settings.wikipedia_client_id == "my_client_id"
        assert settings.wikipedia_client_secret == "my_client_secret"
        assert settings.wikipedia_auth_url == "https://en.wikipedia.org/w/rest.php/oauth2/access_token"
        assert settings.wikipedia_api_url == "https://en.wikipedia.org/api/rest_v1/"

    def test_wikipedia_credentials_empty_defaults(self):
        """Test Wikipedia credentials with empty defaults."""
        settings = Settings()
        
        assert settings.wikipedia_client_id == ""
        assert settings.wikipedia_client_secret == ""
