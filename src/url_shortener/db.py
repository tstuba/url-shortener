from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from url_shortener.settings import settings

DATABASE_URL = settings.database_url

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
