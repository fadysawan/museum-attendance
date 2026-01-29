"""Exception for data processing errors including parsing, extraction, and validation."""

from .museum_data_fetcher_error import MuseumDataFetcherError


class DataProcessingError(MuseumDataFetcherError):
    """Exception for data processing errors including parsing, extraction, and validation."""
    
    def __init__(self, message: str, url: str | None = None, field: str | None = None, value: str | None = None, element: str | None = None, details: dict | None = None):
        self.url = url
        self.field = field
        self.value = value
        self.element = element
        details = details or {}
        if url:
            details['url'] = url
        if field:
            details['field'] = field
        if value:
            details['value'] = value
        if element:
            details['element'] = element
        super().__init__(message, details)
