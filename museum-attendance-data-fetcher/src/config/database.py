"""Database configuration and session management."""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from config.settings import settings
from utils.logging import get_logger

logger = get_logger(__name__)

# Global engine instance (created once, reused)
_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    """Get or create the SQLAlchemy engine with production settings.
    
    Returns:
        Engine: Configured SQLAlchemy engine instance
    """
    global _engine
    
    if _engine is None:
        logger.info(f"Creating database engine for {settings.db_host}:{settings.db_port}/{settings.db_name}")
        
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
    SessionLocal = get_session_maker()
    session = SessionLocal()
    
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def close_db() -> None:
    global _engine
    if _engine is not None:
        logger.info("Closing database connections...")
        _engine.dispose()
        _engine = None
        logger.info("Database connections closed")