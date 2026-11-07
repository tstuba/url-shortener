import logging
import secrets
import string
from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from url_shortener.exceptions import ShortCodeGenerationError
from url_shortener.models.url import Url
from url_shortener.settings import settings

logger = logging.getLogger(__name__)

SHORT_CODE_CONSTRAINT = "uq_urls_short_code"


def is_short_code_collision(exc: IntegrityError) -> bool:
    cause = exc.orig.__cause__

    return (
        getattr(cause, "sqlstate", None) == "23505"
        and getattr(cause, "constraint_name", None) == SHORT_CODE_CONSTRAINT
    )


ALPHABET = string.ascii_letters + string.digits


def generate_short_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(settings.short_code_length))


class ShortUrlService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        code_generator: Callable[[], str],
        max_retries: int,
        url_ttl_days: int,
    ):
        self._session_factory = session_factory
        self._code_generator = code_generator
        self._max_retries = max_retries
        self._url_ttl_days = url_ttl_days

    async def create_short_url(self, target_url: str) -> Url:
        async with self._session_factory() as session:
            for _ in range(self._max_retries):
                url: Url = Url(
                    short_code=self._code_generator(),
                    target_url=target_url,
                    expires_at=datetime.now(timezone.utc)
                    + timedelta(days=self._url_ttl_days),
                )
                session.add(url)

                try:
                    await session.commit()
                    return url
                except IntegrityError as exc:
                    await session.rollback()

                    if not is_short_code_collision(exc):
                        raise
        logger.error(
            "Failed to generate unique short code after %d attempts",
            self._max_retries,
        )
        raise ShortCodeGenerationError("Could not generate unique short code")
