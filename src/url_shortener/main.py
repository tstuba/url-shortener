from fastapi import FastAPI

from url_shortener.schemas import UrlCreateRequestSchema, UrlCreateResponseSchema

app = FastAPI()


@app.get("/health-check")
def chealt_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/url", status_code=201)
async def create_url(request: UrlCreateRequestSchema) -> UrlCreateResponseSchema:
    pass
