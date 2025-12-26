import contextlib
from collections.abc import AsyncIterator

class Container:
    """Dependency Injection Container"""
    
    def __init__(self, settings: BaseAppSettings) -> None:
        self._settings = settings
        self._engine = create_async_engine(**settings.sqlalchemy_engine_props)
        self._session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def lifespan(self) -> AsyncIterator[AsyncSession]:
        """Lifespan context manager for the container."""
        # Initialize resources here (e.g., database connections, caches)
        yield
        # Clean up resources here
