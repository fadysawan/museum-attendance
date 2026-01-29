"""Exception for database-related errors including connections, constraints, and persistence."""

from .museum_data_fetcher_error import MuseumDataFetcherError


class DatabaseError(MuseumDataFetcherError):
    """Exception for database-related errors including connections, constraints, and persistence."""
    
    def __init__(self, message: str, entity_type: str | None = None, entity_id: str | None = None, operation: str | None = None, details: dict | None = None):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.operation = operation
        details = details or {}
        if entity_type:
            details['entity_type'] = entity_type
        if entity_id:
            details['entity_id'] = entity_id
        if operation:
            details['operation'] = operation
        super().__init__(message, details)
