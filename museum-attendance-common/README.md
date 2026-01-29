# Museum Attendance Common

Shared database, logging, and repository components for museum attendance projects.

## Components

- **utils**: Logging utilities with JSON formatter
- **config**: Database configuration and Pydantic settings
- **model**: SQLAlchemy database models (Country, City, Museum, MuseumAttributes, ImportLog)
- **repository**: Data access layer for all models
- **exceptions**: Custom exception hierarchy
- **enumeration**: Shared enumerations (ImportStatus)

## Installation

```bash
pip install -e .
```

## Usage

```python
from museum_attendance_common.config import Settings, get_db_session
from museum_attendance_common.utils import get_logger, setup_logging
from museum_attendance_common.model import Museum, City, Country
from museum_attendance_common.repository import MuseumRepository

# Setup logging
setup_logging(log_level="INFO")
logger = get_logger(__name__)

# Use database session
with get_db_session() as session:
    repo = MuseumRepository(session)
    museum, inserted, updated = repo.get_by_name("Louvre")
```
