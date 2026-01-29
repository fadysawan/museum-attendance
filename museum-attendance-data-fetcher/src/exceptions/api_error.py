"""Exception for API-related errors including authentication, rate limiting, and HTTP errors."""

from .museum_data_fetcher_error import MuseumDataFetcherError


class APIError(MuseumDataFetcherError):
    """Exception for API-related errors including authentication, rate limiting, and HTTP errors."""
    
    def __init__(self, message: str, status_code: int | None = None, url: str | None = None, retry_after: int | None = None, details: dict | None = None):
        self.status_code = status_code
        self.url = url
        self.retry_after = retry_after
        details = details or {}
        if status_code:
            details['status_code'] = status_code
        if url:
            details['url'] = url
        if retry_after:
            details['retry_after'] = retry_after
        super().__init__(message, details)
