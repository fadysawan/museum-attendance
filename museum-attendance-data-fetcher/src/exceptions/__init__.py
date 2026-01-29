"""Custom exceptions module for the Museum Attendance Data Fetcher application.

This module provides a simple hierarchy of exceptions:
- MuseumDataFetcherError: Base exception for all application errors
- APIError: All API-related issues (HTTP errors, auth, rate limiting)
- DatabaseError: All database issues (connections, constraints, persistence)
- DataProcessingError: All data processing issues (parsing, extraction, validation)
- ConfigurationError: Configuration loading and validation errors
"""

from .museum_data_fetcher_error import MuseumDataFetcherError
from .api_error import APIError
from .database_error import DatabaseError
from .data_processing_error import DataProcessingError
from .configuration_error import ConfigurationError

__all__ = [
    'MuseumDataFetcherError',
    'APIError',
    'DatabaseError',
    'DataProcessingError',
    'ConfigurationError',
]
