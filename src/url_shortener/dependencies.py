from typing import Annotated

from fastapi import Depends

from url_shortener.db import SessionFactory
from url_shortener.services import ShortUrlService, generate_short_code
from url_shortener.settings import settings


def get_short_url_service() -> ShortUrlService:
    return ShortUrlService(
        session_factory=SessionFactory,
        code_generator=generate_short_code,
        max_retries=settings.short_code_max_retries,
        url_ttl_days=settings.url_ttl_days,
    )


ShortUrlServiceDep = Annotated[
    ShortUrlService,
    Depends(get_short_url_service),
]
