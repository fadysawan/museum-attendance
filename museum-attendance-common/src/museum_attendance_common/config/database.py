"""Database configuration and session management."""
from contextlib import contextmanager
from typing import Generator
import time

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from museum_attendance_common.config.settings import Settings
from museum_attendance_common.utils.logging import get_logger
from museum_attendance_common.exceptions import DatabaseError

logger = get_logger(__name__)
settings = Settings()

# Global engine instance (created once, reused)
_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    """Get or create the SQLAlchemy engine with production settings.

    Returns:
        Engine: Configured SQLAlchemy engine instance

    Raises:
        DatabaseError: If engine creation fails
    """
    global _engine

    if _engine is None:
        try:
            logger.info(f"Creating database engine: {settings.db_host}:{settings.db_port}/{settings.db_name}")
            
            start_time = time.time()
            _engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                pool_timeout=settings.db_pool_timeout,
                pool_recycle=settings.db_pool_recycle,
                pool_pre_ping=True,
                echo=False,
            )

            # Test the connection
            with _engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            elapsed_time = time.time() - start_time
            logger.info(f"Database engine created in {elapsed_time:.2f}s")

        except OperationalError as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise DatabaseError(
                f"Cannot connect to database at {settings.db_host}:{settings.db_port}/{settings.db_name}",
                details={"error": str(e)}
            ) from e

        except Exception as e:
            logger.error(f"Failed to create database engine: {str(e)}")
            raise DatabaseError(
                f"Failed to create database engine: {str(e)}",
                details={"error": str(e)}
            ) from e

    return _engine


def get_session_maker() -> sessionmaker:
    """Get or create the session maker.

    Returns:
        sessionmaker: Configured session factory
    """
    global _SessionLocal

    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False,
        )

    return _SessionLocal


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session with automatic transaction management.

    Yields:
        Session: Database session

    Raises:
        DatabaseError: If database operations fail
    """
    SessionLocal = get_session_maker()
    session = SessionLocal()
    start_time = time.time()

    try:
        yield session
        session.commit()
        
        elapsed_time = time.time() - start_time
        operation_count = len(session.new) + len(session.dirty) + len(session.deleted)
        if operation_count > 0:
            logger.debug(f"Transaction committed: {operation_count} operations in {elapsed_time:.2f}s")

    except SQLAlchemyError as e:
        session.rollback()
        elapsed_time = time.time() - start_time
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)
        logger.error(f"Database error after {elapsed_time:.2f}s: {error_msg}")
        raise DatabaseError(
            f"Database operation failed: {error_msg}",
            operation="commit",
            details={"error": error_msg, "elapsed_time": elapsed_time}
        ) from e

    except Exception as e:
        session.rollback()
        elapsed_time = time.time() - start_time
        logger.error(f"Unexpected error after {elapsed_time:.2f}s: {str(e)}")
        raise DatabaseError(
            f"Unexpected database error: {str(e)}",
            operation="commit",
            details={"error": str(e), "elapsed_time": elapsed_time}
        ) from e

    finally:
        session.close()


def close_db() -> None:
    """Close database connections and dispose of the engine."""
    global _engine, _SessionLocal

    if _engine is not None:
        try:
            logger.info("Closing database connections...")
            _engine.dispose()
            _engine = None
            _SessionLocal = None
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database: {str(e)}")
    else:
        logger.debug("No database engine to close")
