import contextlib
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings

class Container:
    """Dependency Injection Container"""
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine = create_engine(
            settings.DATABASE_URL,
            pool_size=10,
            max_overflow=20
        )
        self._session_factory = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)

    @contextlib.contextmanager
    def session(self) -> Iterator[Session]:
        """Provide a transactional scope around a series of operations."""
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
