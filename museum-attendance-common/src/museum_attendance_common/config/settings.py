from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    db_user: str = "IL_USER"
    db_password: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "museum_attendance"
    
    # Database connection pool settings
    db_pool_size: int = 1           # Only 1 connection needed
    db_max_overflow: int = 0        # No overflow needed
    db_pool_timeout: int = 30       # Keep this
    db_pool_recycle: int = 3600     # Keep this (prevents stale connections)

    keep_html_files: bool = False

    # rate limiting for wikipedia API
    rate_limit_calls: int = 2
    rate_limit_period: int = 1

    # multithreading settings
    max_workers: int = 5
    
    # wikipedia API credentials
    wikipedia_auth_url: str = "https://en.wikipedia.org/w/rest.php/oauth2/access_token"
    wikipedia_api_url: str = "https://en.wikipedia.org/api/rest_v1/"
    wikipedia_client_id: str = ""
    wikipedia_client_secret: str = ""

    # Application settings
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=Path(".env"), env_file_encoding="utf-8")

    @property
    def database_url(self) -> URL:
        """Build database URL with properly encoded credentials."""
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        )