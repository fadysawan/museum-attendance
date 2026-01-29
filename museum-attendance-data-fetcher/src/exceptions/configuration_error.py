"""Exception raised for configuration loading or validation errors."""

from .museum_data_fetcher_error import MuseumDataFetcherError


class ConfigurationError(MuseumDataFetcherError):
    """Exception raised for configuration loading or validation errors."""
    
    def __init__(self, message: str, setting_name: str | None = None, details: dict | None = None):
        self.setting_name = setting_name
        details = details or {}
        if setting_name:
            details['setting_name'] = setting_name
        super().__init__(message, details)
