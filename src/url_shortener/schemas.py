from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UrlCreateRequestSchema(BaseModel):
    target_url: HttpUrl


class UrlCreateResponseSchema(BaseModel):
    short_code: str
    short_url: HttpUrl
    target_url: HttpUrl
    created_at: datetime
    expires_at: datetime | None
