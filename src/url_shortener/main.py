from fastapi import FastAPI, HTTPException

from url_shortener.dependencies import ShortUrlServiceDep
from url_shortener.exceptions import ShortCodeGenerationError
from url_shortener.schemas import UrlCreateRequestSchema, UrlCreateResponseSchema
from url_shortener.settings import settings

app = FastAPI(
    title=settings.title,
    debug=settings.debug,
)


@app.get("/health-check")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/urls", status_code=201)
async def create_url(
    payload: UrlCreateRequestSchema,
    service: ShortUrlServiceDep,
) -> UrlCreateResponseSchema:
    try:
        url = await service.create_short_url(
            target_url=str(payload.target_url),
        )
    except ShortCodeGenerationError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
    return UrlCreateResponseSchema(
        short_code=url.short_code,
        short_url=f"{settings.public_base_url}/{url.short_code}",
        target_url=url.target_url,
        created_at=url.created_at,
        expires_at=url.expires_at,
    )
